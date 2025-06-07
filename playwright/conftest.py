import pytest
import json

@pytest.fixture()
def login_vars():
    with open("login_vars.json", 'r') as file:
        data = json.load(file)
    
    yield data
    
@pytest.fixture()
def log():
    with open("thegreatcleansing.log", 'a+') as file:
        yield file

@pytest.fixture()
def followers_list():
    with open("followers_1.json", 'r') as file:
        data = json.load(file)
    
    yield data