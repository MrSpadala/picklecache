"""
Run some tests
"""

from pklcache import cache
import os

fname = "test_cache.pkl"

def rm_if_present():
    if os.path.isfile(fname):
        os.remove(fname)

def cleanup(func):
    def wrapper(*args, **kwargs):
        rm_if_present()
        func(*args, **kwargs)
        rm_if_present()
    return wrapper


@cleanup
def test1():
    @cache(fname)
    def foo():
        ret = [(69,96), "who cares about types", 42, [4,2,0]]
        return ret

    # Call foo two times, the first is executed and saves the 
    # result on disk, the second time it just loads the data
    ret = foo()  
    ret_cached = foo()

    assert(ret==ret_cached)
    assert(os.path.isfile(fname))
    print("Test 1: OK")


@cleanup
def test2():
    @cache(fname, enabled=False)
    def foo1():
        ret = "nope"
        return ret

    ret = foo1()
    assert(not os.path.isfile(fname))
    print("Test 2: OK")


if __name__ == '__main__':

    test1()

    test2()




