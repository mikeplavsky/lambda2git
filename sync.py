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

git_url = "https://api.github.com/repos/%s/contents/%s"

l = boto3.client("lambda")

def get_file(path):

    res = requests.get(
            
            git_url % (git_repo,path),
            auth=(git_user,git_key))

    return res


def create_file(
        path,
        message,
        text):

    res = requests.put(
            
            git_url % (git_repo,path),
            auth=(git_user,git_key),

            json=dict(
                message=message,
                sha = "e30eaeba4c5f728122df548f34c1d9e258a9ae5e",
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

    zf = open(
            tf.name + ".zip/" + ns[0])

    return zf.read()


def run():

    vs = l.list_versions_by_function(
            FunctionName="aws-cleaner-sg")

    print(len(vs["Versions"]))

    for v in vs["Versions"]:

        print(v)
        
        fn = v["FunctionArn"]

        print(fn)

        print(v["Version"])
        print(v["Description"])

        text = get_function(fn)

        import hashlib
        r = hashlib.sha1()

        r.update(text)
        print(r.hexdigest())

        return text

        msg = v["Description"]
        name = v["FunctionName"] + ".py"

        res = create_file(name, msg, text )
        return res







