from nose.tools import eq_
from sync import get_ext, get_versions, get_init_state

def test_file_was_removed():

    sha, start, commit_msg = get_init_state(
            None, [1,2,3,4,5])

    eq_(sha,None)
    eq_(start,True)
    eq_(commit_msg,None)
    
def test_commits_and_file():

    sha, start, commit_msg = get_init_state(
            dict(sha="abcd"),
            [dict(
                commit=dict(
                    message="description\nCodeSha256")),
                "5","77"])

    eq_(sha,"abcd")
    eq_(start,False)
    eq_(commit_msg,"CodeSha256")

def test_no_commits():

    sha, start, commit_msg = get_init_state(
            "file", [])

    eq_(sha,None)
    eq_(start,True)
    eq_(commit_msg,None)

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

