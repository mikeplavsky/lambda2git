import boto3

def run():

    l = boto3.client("lambda")
    f = l.get_function(FunctionName="aws-cleaner-sg")

    print(f)


