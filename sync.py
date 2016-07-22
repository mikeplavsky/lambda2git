import boto3
import urllib2
import zipfile
from tempfile import NamedTemporaryFile

import os

git_key = os.environ.get("GIT_KEY")
git_url = "https://api.github.com/repos/GitQuest/aws-police/contents/README.md"

l = boto3.client("lambda")

def create_file():

    import urllib2
    
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    
    req = urllib2.Request(git_url,data="")
    req.get_method = lambda: "PUT"

    url = opener.open(req)


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







