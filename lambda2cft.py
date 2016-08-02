cf = dict(
    AWSTemplateFormatVersion = "2010-09-09",
    Resources = {})

def generate(funcs):

    from sync import get_function
    import json

    for f in funcs:

        code,func = get_function(f)
        func = func["Configuration"]

        res = {f:dict(

            Type = "AWS::Lambda::Function",

            Properties = dict(

                Code = dict(ZipFile=code),

                Handler=func["Handler"],
                Runtime=func["Runtime"],
                Description=func["Description"],
                FunctionName=func["FunctionName"],
                MemorySize=func["MemorySize"],
                Role=func["Role"],
                Timeout=func["Timeout"]

            ))}

        cf["Resources"].update(res)

    return cf
