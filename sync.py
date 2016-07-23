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
get_file = lambda path: get_command("contents", path)

def reate_file(
        path,
        message,
        text,
        sha=""):

    res = requests.put(
            
            git_contents % (git_repo,path),
            auth=(git_user,git_key),

            json=dict(
                message=message,
                sha = sha,
                content=base64.b64encode(text)))

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

    vs = l.list_versions_by_function(
            FunctionName="aws-cleaner-sg")

    for v in vs["Versions"]:

        fn = v["FunctionArn"]
        print(v)

        text = get_function(fn)

        msg = v["Description"] 
        msg = msg + "\n" + v["CodeSha256"] 

        name = v["FunctionName"] + ".py"

        res = create_file(name, msg, text )
        return res







