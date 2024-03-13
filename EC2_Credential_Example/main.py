from fastapi import FastAPI
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import json
import jwt
import boto3


app = FastAPI()

def get_secret():

    secret_name = "cloud/jwt/example"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

@app.get("/")
async def root(request: Request):
    s = get_secret()
    print("Secret = ", s)

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)

