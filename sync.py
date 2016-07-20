import boto3

def run():

    l = boto3.client("lambda")

    vs = l.list_versions_by_function(
            FunctionName="aws-cleaner-sg")

    print(len(vs["Versions"]))

    for v in vs["Versions"]:
        
        fn = v["FunctionArn"]

        print(fn)

        print(v["Version"])
        print(v["Description"])

        f = l.get_function(
                FunctionName=fn)

        print(f["Code"]["Location"])



