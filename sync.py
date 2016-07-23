import boto3
import urllib2
import zipfile
from tempfile import NamedTemporaryFile

import os

git_user = os.environ.get("GIT_USER")
git_key = os.environ.get("GIT_KEY")
git_repo = os.environ.get("GIT_REPO")

git_url = "https://api.github.com/repos/%s/contents/%s"

l = boto3.client("lambda")

def create_file():

    text = "it is cool!"
    import base64
    
    import requests

    res = requests.put(
            
            git_url % (git_repo, "README1.md"),
            auth=(git_user,git_key),

            json=dict(
                message="checking...",
                sha = "419861053327af2a12d5c8769153a4571da2f96b",
                content=base64.b64encode(text)))

    return res



def get_function(fn):

    f = l.get_function(
            FunctionName=fn)

    loc = f["Code"]["Location"]
    print(loc)
    
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

    zf = open(tf.name + ".zip/" + ns[0])
    print(zf.read())


def run():

    vs = l.list_versions_by_function(
            FunctionName="aws-cleaner-sg")

    print(len(vs["Versions"]))

    for v in vs["Versions"]:
        
        fn = v["FunctionArn"]

        print(fn)

        print(v["Version"])
        print(v["Description"])

        get_function(fn)







