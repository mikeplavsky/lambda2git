import sys
sys.path.append("packages")

import boto3
import urllib2
import zipfile
from tempfile import NamedTemporaryFile

import os
import requests
import base64

git_user = None 
git_key = None
git_repo = None

git_url = "https://api.github.com/repos/%s/%s?path=%s"
git_contents = "https://api.github.com/repos/%s/contents/%s"

l = boto3.client("lambda")

def lambda_handler(event, context):

    global git_user, git_key, git_repo

    git_user = event["GIT_USER"]
    git_key = event["GIT_KEY"]
    git_repo = event["GIT_REPO"]

    aws_lambda = event["AWS_LAMBDA"]
    sync(aws_lambda)

def get_command(command, path):

    res = requests.get(
            
            git_url % (git_repo,command,path),
            auth=(git_user,git_key))

    res.raise_for_status()
    return res

get_commits = lambda path: get_command("commits", path)

def get_file(path): 

    res = requests.get(
            
            git_contents % (git_repo,path),
            auth=(git_user,git_key))

    res.raise_for_status()
    return res

def create_file(
        path,
        message,
        text,
        sha=None):

    json = dict(
        message=message,
        sha = sha,
        content=base64.b64encode(text))

    if not sha: 
        del json['sha']

    res = requests.put(
            
            git_contents % (git_repo,path),
            auth=(git_user,git_key),
            json=json)

    res.raise_for_status()
    return res

def get_function(fn):

    f = l.get_function(
            FunctionName=fn)

    loc = f["Code"]["Location"]
    
    code = urllib2.urlopen(loc)
    zip_code = code.read()

    tf = NamedTemporaryFile()

    tf.write(zip_code)
    tf.flush()

    import zipfile

    z = zipfile.ZipFile(tf.name, 'r', zipfile.ZIP_STORED)
    z.extractall(path=tf.name + ".zip")

    tf.close()

    ns = z.namelist()

    zf = open(
            tf.name + ".zip/" + ns[0])

    return (zf.read(),f)

def run(aws_lambda):

    global git_user, git_key, git_repo

    git_user = os.environ["GIT_USER"]
    git_key = os.environ["GIT_KEY"]
    git_repo = os.environ["GIT_REPO"]

    sync(aws_lambda)

def get_ext(runtime):

    ext = ""

    if "python" in runtime:
        ext = ".py"
    elif "nodejs" in runtime:
        ext = ".js"

    return ext

def get_versions(vs):

    vers = vs[1:]
    
    if len(vers): 
        
        if vs[0]["CodeSha256"] != vs[-1]["CodeSha256"]:  

            print("$LATEST was not published.")
            vers.append(vs[0])

        else:
            print("$LATEST was published.")

    if not len(vers):

        print("Nothing was published.")
        vers.append(vs[0])

    return vers

def get_init_state(f, commits):

    sha = None
    start = True
    commit_msg = None

    if len(commits) and f: 

        start = False

        sha = f["sha"]
        commit_msg = commits[0]["commit"]["message"]
        
        commit_msg = commit_msg.split("\n")[1]

        print("looking for")
        print(commit_msg)

        print("sha in github")
        print(sha)

    return sha, start, commit_msg

def sync(aws_lambda):

    la = l.get_function(
            FunctionName=aws_lambda)

    ext = get_ext(
            la["Configuration"]["Runtime"])

    name = aws_lambda + ext
    print("Syncing " + name)

    commits = get_commits(name).json()
    print("Commits: %s" % len(commits))

    f = None

    try:
        f = get_file(name).json()
    except Exception as ex:
        print(ex)

    sha, start, commit_msg = get_init_state(f,commits)
    
    vs = l.list_versions_by_function(
            FunctionName=aws_lambda)["Versions"]

    vers = get_versions(vs)
    started_sync = False

    for v in vers:

        msg = v["Description"] 
        msg = msg + "\n" + v["CodeSha256"] 

        print(msg)
        
        if start:
            
            started_sync = True

            fn = v["FunctionArn"]
            text,_ = get_function(fn)

            res = create_file(
                    name, msg, text, sha).json()

            sha = res["content"]["sha"]

        if len(commits) and commit_msg == v["CodeSha256"]:

            print("found last commit")
            start = True

    if len(vers) and not started_sync:
        print("It seems nothing to sync.")

    if len(vers) and not start:
        print("Something is wrong. Last commit was not found.")









