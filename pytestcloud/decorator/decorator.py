import logging
"""
函数作为变量，传到函数
"""
def use_logging(func):
    logging.warning("%s is running" % func.__name__)
    func()

def foo():
    print('i am foo')

use_logging(foo)



"""
简单装饰器
"""
def use_logging2(func):

    def wrapper():
        logging.warning("%s is running" % func.__name__)
        return func() # 要执行所以有括号
    return wrapper #返回到是函数对象，所以不需要括号

@use_logging2
def foo2():
    print("i am foo2")
foo2()


"""
函数有参数到装饰器
"""
def use_logging3(func):

    def wrapper(*args, **kwargs):
        logging.warning("%s is running" % func.__name__)
        return func(*args, **kwargs)
    return wrapper

@use_logging3
def foo3(name, age=None, height=None):
    print("I am %s, age %s, height %s" % (name, age, height))

foo3("sharon", "18")

"""
带参数的装饰器
"""
def use_logging4(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warning("%s is running" % func.__name__)
            elif level == "info":
                logging.warning("%s is running" % func.__name__)
            return func(*args, **kwargs)

        return wrapper
    return decorator

@use_logging4(level="info")
def foo4(name='foo'):
    print("i am %s" % name)

foo4()


"""
类装饰器
"""
class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print('class decorator runing')
        self._func()
        print('class decorator ending')

@Foo
def bar():
    print('bar')

bar()

"""
被装饰函数的元信息不被替换
"""
from functools import wraps
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print("name is %s" % func.__name__)
        print("doc is %s" % func.__doc__)
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
    return x + x * x

f(4)

"""
装饰器顺序：从下往上（从里往外）
"""