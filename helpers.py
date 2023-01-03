import os
# For regex, for checking email validation
import re
# For UUID to generate uuids easily and automatically for objects
from uuid import uuid4
# For password hashing
import hashlib
# For encoding strings
import base64
# For date/time manipulation
from datetime import datetime, timedelta, timezone


# A helper to get an env variable with a fallback
def get_env_variable(env_variable_name, fallback=False):
    if env_variable_name in os.environ:
        return os.getenv(env_variable_name)
    return fallback


# Simple auto-uuid helper for setting on model ID fields
def getUUID():
    return str(uuid4())


# Simple auto-uuid helper for setting on api_key ID fields
def getDoubleUUID():
    return getUUID() + "-" + getUUID()


# Get an locational timezone object that is HOURS in the future for use in TTL Expiration on DynamoDB
def getTTLExpiration(hours = 24):
    dt = datetime.now() + timedelta(hours=hours)
    return dt.replace(tzinfo=timezone.utc)


# Simple email syntax validation
def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False


# Get the AWS region we are running/deployed in AWS Lambda (or locally use hardcoded us-east-1 as internal/default)
def get_deployed_region():
    return get_env_variable('AWS_REGION', "us-east-1")


# Get the AWS DynamoDB Endpoint
def get_dynamodb_endpoint():
    return get_env_variable('DYNAMO_ENDPOINT', "dynamodb.{}.amazonaws.com".format(get_deployed_region()))


# Encode and decode JSON, for bytes or string...
def base64_encode(input_string):
    if type(input_string) is bytes:
        return str(base64.b64encode(input_string).decode("ascii"))
    if type(input_string) is str:
        return str(base64.b64encode(input_string.encode("ascii")).decode("ascii"))
def base64_decode(input_string):
    return base64.b64decode(input_string).decode("ascii")


# Hash a password with our preferred algorithm, sha256
def hash_password(password, salt = None):
    rounds = 100000
    if salt is None:
        salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, rounds)
    return salt, hashed
