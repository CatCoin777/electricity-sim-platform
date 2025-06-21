# mock_users.py

mock_users = {
    "student1": {
        "username": "student1",
        "full_name": "张三",
        "role": "student",
        "hashed_password": "123456"
    },
    "teacher1": {
        "username": "teacher1",
        "full_name": "李老师",
        "role": "teacher",
        "hashed_password": "admin"
    }
}


def add_mock_user(user_dict):
    username = user_dict["username"]
    if username in mock_users:
        return False
    mock_users[username] = user_dict
    return True
