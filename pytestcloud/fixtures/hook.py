import logging
import pytest


@pytest.fixture(scope="module", autouse="True")
def case_module_hook(request, app):
    """
    automatically call 'before_module(app) and after_module(app)'
    once call for each module
    """
    if request.module is None:
        return

    ns = '%s.py' % request.module.__name__
    fn_call(request.module, 'before_module', 'SETUPING', ns, app)

    def module_teardown():
        fn_call(request.module, 'after_module', 'CLEANUPING', ns, app)
        print('COMPLETED %s' % ns)
    request.addfinalizer(module_teardown)


@pytest.fixture(scope="class", autouse="True")
def case_class_hook(request, app):
    """
    automatically call 'before_class(cls, app) and after_class(cls, app)'
    once call for each class
    """
    if request.cls is None:
        return

    ns = '%s.py::%s' % (request.module.__name__, request.cls.__name__)
    print('STARTING %s' % ns)
    fn_call(request.cls, 'before_class', 'SETUPING', ns, app)

    def cls_teardown():
        fn_call(request.cls, 'after_class', 'CLEANUPING', ns, app)
        print('COMPLETED %s' % ns)

    request.addfinalizer(cls_teardown)


@pytest.fixture(scope='function', autouse="True")
def case_function_hook(request, app):
    """
    automatically call cleanup_<class_name>(self, app) after call test_<case_name>(...)
    automatically call before_each_func(self, app) and after_each_func(self, app)
    once call for each function
    """
    ns = request.module.__name__ + ".py"
    if request.cls is not None:
        ns = ns + "::" + request.cls.__name__
    fn_name_case = request.function.__name__
    fn_name_cleanup = 'cleanup_' + request.function.__name__[5:]

    fn_parent_object = request.cls
    if request.cls is None:
        fn_parent_object = request.module

    fn_call(fn_parent_object, 'before_each_func', 'SETUPING', ns, app, request.instance)

    def func_teardown():
        fn_call(fn_parent_object, fn_name_cleanup, 'CLEANUPING', ns, app, request.instance)
        fn_call(fn_parent_object, 'after_each_func', 'CLEANUPING', ns, app,request.instance)
        print("COMPLETED %s::%s" % (ns, fn_name_case))

    request.addfinalizer(func_teardown)


def fn_call(fn_parent_obj, fn_name, action, ns, app, instance=None):
    fn = getattr(fn_parent_obj, fn_name, None)
    if fn is None:
        return

    print('%s %s::%s' % (action, ns, fn_name))

    if instance is None:
        fn(app)
    else:
        fn(instance, app)
