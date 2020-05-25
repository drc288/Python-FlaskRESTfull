#!/usr/bin/python3.8
from werkzeug.security import safe_str_cmp
from user import User
users = [
    User(1, 'bob', '123')
]

username_mapping: dict = {u.username: u for u in users}
userid_mapping: dict = {u.id: u for u in users}


def authenticate(username: str, password: str) -> dict:
    """
    Authenticate the user, use safe_str_cmp to compare two string
    this can y any proyect
    :param username: user
    :param password: pass
    :return: None or the user
    """
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload: dict) -> dict:
    """
    Peyload the user and verify if this exists
    :param payload: data map
    :return: none or the user
    """
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)