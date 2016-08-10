from nose.tools import eq_
from sync import get_ext, get_versions

def test_nothing_was_published():
    
    vs = [dict(CodeSha256=3)]

    res = get_versions(vs)
    eq_(res, [dict(CodeSha256=3)])

def test_latest_was_not_published():
    
    vs = [dict(CodeSha256=3),
            dict(CodeSha256=0),
            dict(CodeSha256=1)]

    res = get_versions(vs)

    eq_(res, [
        dict(CodeSha256=0), 
        dict(CodeSha256=1),
        dict(CodeSha256=3)])

def test_latest_was_published():
    
    vs = [dict(CodeSha256=1),
            dict(CodeSha256=0),
            dict(CodeSha256=1)]

    res = get_versions(vs)

    eq_(res, [
        dict(CodeSha256=0), 
        dict(CodeSha256=1)])

def test_file_extension():

    runtime = [
            (["python"], ".py"),
            (["nodejs"], ".js"),
            (["java"], "")]

    for r,v in runtime:
        
        res = get_ext(r)
        eq_(res, v)

