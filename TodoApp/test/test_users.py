from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/Users/Users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithrobytest'
    assert response.json()['email'] == 'codingwithrobytest@email.com'
    assert response.json()['id'] == 1
    assert response.json()['role'] == 'admin'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['phone_number'] == '+1 111-11-11'
    assert response.json()['is_active'] == True


def test_change_password_success(test_user):
    response = client.put("/Users/password", json={"password": "testpassword",
                                                   "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/Users/password", json={"password": "wrong_password",
                                                   "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Password mismatch'}


def test_change_phone_number_success(test_user):
    response = client.put("/Users/22222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT