cf = dict(
    AWSTemplateFormatVersion = "2010-09-09",
    Resources = {})

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
                Role=func["Role"],
                Timeout=func["Timeout"]

            ))}

        cf["Resources"].update(res)

    return json.dumps(cf,indent=4,sort_keys=True)
