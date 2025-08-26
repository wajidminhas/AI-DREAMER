
import requests
from agents import function_tool


@function_tool
async def fetch_users()-> list:
    """ Fetch the data of all user or which user is asked"""
    print("this is the data of all user with fetch users tool.")
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    return response.json()

@function_tool
def fetch_user_by_id(id :int) ->list:
    """fetch the function and give the data of user by his id"""
    url = f"https://jsonplaceholder.typicode.com/users/{id}"

    res = requests.get(url)
    print(f"this is the data of user with fetch user by id tool.")
    return res.json()