#
# some of this code comes from the snippet produced by the AWS console
# when creating a secret.
#
import json

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name="us-east-1"):
    """
    Retrieve a secret. The function checks if the secret is serialized JSON and
    converts to a dictionary if it is. Otherwise, returns the secret string.

    :param secret_name: Name of the secret.
    :param region_name: Region in which the secret is stored in the secrets manager.
    :return: The JSON or string secret.
    """

    # Create a Secrets Manager client.
    #
    # NOTE: For this to work, the API Key and Secret must be in the environment or
    # default location.
    #
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

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    final_secret = secret

    # try to convert the secret to JSON/dictionary.
    try:
        final_secret = json.loads(secret)
    except json.JSONDecodeError:
        # Not JSON
        final_secret = secret

    return final_secret


if __name__ == "__main__":
    secret_name = "cloud/jwt/example"
    print("Try to get the secret named", secret_name)
    the_secret = get_secret(secret_name)

    print("The secret is: \n", json.dumps(the_secret, indent=2))



