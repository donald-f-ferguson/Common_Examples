from fastapi import FastAPI
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import json
import jwt

secret = "12345"
session_header_key = "cool_stuff"

session_storage = dict()

app = FastAPI()


class User(BaseModel):
    user_name: str


class Value(BaseModel):
    to_add: int


def add_stateful(session_key, added_value):
    value = session_storage.get(session_key, 0)
    value += added_value
    session_storage[session_key] = value
    return value


def add_count(session_info: dict, count):

    if session_info is None:
        session_info = dict()

    session_info["count"] = count

    return session_info


@app.post("/current_user")
def current_user(u: User) -> JSONResponse:
    user_name = u.user_name
    rsp_headers = {"user_name": user_name}
    result = JSONResponse({"status": "OK"}, 201, headers=rsp_headers)
    return result


@app.get("/stateful_adder")
def stateful_adder(request: Request, added_value: int) -> JSONResponse:
    session_key = request.headers.get("user", None)
    if session_key:
        new_value = add_stateful(session_key, added_value)
        rsp = {"new_value": new_value}
        response = JSONResponse(content=rsp, status_code=200, headers={"user": session_key})
    else:
        response = JSONResponse(content="User not set.", status_code=403)

    return response


@app.get("/stateless_adder")
def stateful_adder(request: Request, added_value: int) -> JSONResponse:
    session_key = request.headers.get("user", None)
    if session_key:
        current_value = request.headers.get("current_value", 0)
        current_value = int(current_value)
        current_value += added_value
        rsp = {"new_value": current_value}
        response = JSONResponse(content=rsp, status_code=200,
                                headers={"user": session_key, "current_value": str(current_value)})
    else:
        response = JSONResponse(content="User not set.", status_code=403)

    return response


@app.get("/")
async def root(request: Request):
    """count = get_count(request)
    print("Count = ", count)
    count += 1
    session_info = add_count(count)
    """

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)

