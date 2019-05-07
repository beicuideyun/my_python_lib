import pytest
class TestDemo1:
    def before_each_func(self, app):
        print("before hahahah.")

    def after_each_func(self, app):
        print("after hahahah.")

    def test_case1(self):
        print("running test case1")

