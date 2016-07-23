import boto3
import urllib2
import zipfile
from tempfile import NamedTemporaryFile

import os
import requests
import base64

git_user = os.environ.get("GIT_USER")
git_key = os.environ.get("GIT_KEY")
git_repo = os.environ.get("GIT_REPO")


git_url = "https://api.github.com/repos/%s/%s?path=%s"
git_contents = "https://api.github.com/repos/%s/contents/%s"

l = boto3.client("lambda")

def get_command(command, path):

    res = requests.get(
            
            git_url % (git_repo,command,path),
            auth=(git_user,git_key))

    return res

get_commits = lambda path: get_command("commits", path)

def get_file(path): 

    res = requests.get(
            
            git_contents % (git_repo,path),
            auth=(git_user,git_key))

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

    return zf.read()

def run():

    aws_lambda = os.environ.get("AWS_LAMBDA")
    sync(aws_lambda)


def sync(aws_lambda):

    name = aws_lambda + ".py"
    commits = get_commits(name).json()

    sha = None
    start = True
    commit_msg = None

    if len(commits):

        f = get_file(name).json()

        start = False
        sha = f["sha"]
        commit_msg = commits[0]["commit"]["message"]

        print("looking for")
        print(commit_msg)

        print("sha in github")
        print(sha)
    
    vs = l.list_versions_by_function(
            FunctionName=aws_lambda)

    for v in vs["Versions"]:

        if v["Version"] == "$LATEST":

            print("skipping $LATEST")
            continue

        msg = v["Description"] 
        msg = msg + "\n" + v["CodeSha256"] 

        print(msg)
        
        if start:
            
            fn = v["FunctionArn"]
            text = get_function(fn)

            res = create_file(
                    name, msg, text, sha).json()

            sha = res["content"]["sha"]

        if len(commits) and commit_msg == msg:

            print("found last commit")
            start = True










