import pytest
from app import APP

@pytest.fixture(scope="session", autouse=True)
def app(request):
    print("lalalal")