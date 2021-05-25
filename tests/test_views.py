from starlette.testclient import TestClient
from requests.auth import HTTPBasicAuth
from app.views import app
import requests, os

client = TestClient(app)
username = os.getenv('USER')
password = os.getenv('PASSWORD')


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello DaftCode'}


def test_read_messages():
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() != {}


def test_post_message():
    response = requests.post('http://127.0.0.1:8000/add_message',
                             json={"Message": "test_db"},
                             auth=HTTPBasicAuth(username, password))
    assert response.status_code == 201


def test_post_message_uu():
    response = requests.post('http://127.0.0.1:8000/add_message',
                             json={"Message": "test_db"},
                             auth=HTTPBasicAuth('BadUser', 'badpassword'))
    assert response.status_code == 401


def test_read_message():
    response = client.get("/messages/5")
    assert response.status_code == 200
    assert response.json() == {
        "message": {
            "Message": "test_db",
            "MessageID": 5,
            "Views": 1,
            }
        }


def test_user():
    response = requests.get('http://127.0.0.1:8000/users/me', auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_bad_user():
    response = requests.get('http://127.0.0.1:8000/users/me', auth=HTTPBasicAuth('BadUser', 'examplepassword'))
    assert response.status_code == 401


def test_update_message():
    response = requests.put('http://127.0.0.1:8000/update_message/5',
                            json={"Message": 'update'},
                            auth=HTTPBasicAuth(username, password),
                            )
    response_1 = client.get("/messages/5")
    assert response.status_code == 200
    assert response_1.json() == {
        "message": {
            "Message": "update",
            "MessageID": 5,
            "Views": 1,
        }
    }


def test_update_empty_message():
    response = requests.put('http://127.0.0.1:8000/update_message/5',
                            json={"Message": ''},
                            auth=HTTPBasicAuth(username, password),
                            )
    assert response.status_code == 406


def test_post_empty_message():
    response = requests.post('http://127.0.0.1:8000/add_message',
                             json={"Message": " "},
                             auth=HTTPBasicAuth(username, password))
    assert response.status_code == 406


def test_views():
    response = client.get("/messages/5")
    assert response.status_code == 200
    assert response.json() == {
        "message": {
            "Message": "update",
            "MessageID": 5,
            "Views": 2,
            }
        }


def test_update_message_uu():
    response = requests.put('http://127.0.0.1:8000/update_message/5',
                            json={"Message": 'update'},
                            auth=HTTPBasicAuth('BadUser', 'badpassword'),
                            )
    assert response.status_code == 401


def test_delete_message_uu():
    response = requests.delete('http://127.0.0.1:8000/delete_message/5',
                               auth=HTTPBasicAuth('BadUser', 'badpassword')
                               )
    assert response.status_code == 401


def test_delete_message():
    response = requests.delete('http://127.0.0.1:8000/delete_message/5',
                               auth=HTTPBasicAuth(username, password)
                               )
    assert response.status_code == 204
