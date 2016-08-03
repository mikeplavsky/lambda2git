cf = dict(
    AWSTemplateFormatVersion = "2010-09-09",
    Resources = dict())

LambdasRole = dict(
    
    Type = "AWS::IAM::Role",

    Properties = dict(
        ManagedPolicyArns = [
            'arn:aws:iam::aws:policy/AWSLambdaFullAccess'],
        AssumeRolePolicyDocument=dict(
            Version = '2012-10-17',
            Statement=[
                dict(

                    Action="sts:AssumeRole",
                    Effect="Allow",
                    Principal = dict(
                        Service = 'lambda.amazonaws.com'),
                    Sid=''

                    )])))

cf["Resources"].update(
        dict(LambdasRole=LambdasRole))

def generate(funcs, prefix=""):

    from sync import get_function
    import json

    for i,f in enumerate(funcs):

        code,func = get_function(f)
        func = func["Configuration"]

        res = {"func%s"%i:dict(

            Type = "AWS::Lambda::Function",

            Properties = dict(

                Code = dict(ZipFile=code),

                Handler="index." + func["Handler"].split(".")[1],

                Runtime=func["Runtime"],
                Description=func["Description"],
                FunctionName=func["FunctionName"] + prefix,
                MemorySize=func["MemorySize"],
                Role=dict(Ref="LambdasRole"),
                Timeout=func["Timeout"]

            ))}

        cf["Resources"].update(res)

    return json.dumps(cf,indent=4,sort_keys=True)
