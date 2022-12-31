# For imports/exceptions see: https://github.com/aws/chalice/blob/master/chalice/__init__.py
from chalice import Chalice, BadRequestError, ConflictError, NotFoundError, Response
from botocore.client import ClientError
from models.User import User
import copy

app = Chalice(app_name='chalice-pynamodb-bootstrap')


# Our health check, for Docker/development purposes, mostly
@app.route('/healthy')
def healthy():
    return {'healthy': True}


# Create an new user object
@app.route('/users', methods=['POST'])
def create_user():
    # Validate not a duplicate
    try:
        user = User.getByIndex('email', app.current_request.json_body['email'])
        raise ConflictError('This email already exists in our system')
    except ClientError as e:
        if "ResourceNotFoundException" not in str(e):
            raise

    # Create the object via helper and return the results to the user with the right HTTP code
    return Response(
        body=User.createFromDict(app.current_request.json_body).to_json(),
        status_code=201
    )


# Get an user object
@app.route('/users/{id}', methods=['GET'])
def get_user(id):
    # Validate input id is valid
    try:
        user = User.get(id)
    except:
        raise NotFoundError("This id was not found in our system")
    return user.to_json()


# Update an user object
@app.route('/users/{id}', methods=['PUT', 'PATCH'])
def update_user(id):
    # Validate input id is valid
    try:
        user = User.get(id)
    except:
        raise NotFoundError("This id was not found in our system")

    # Update attributes
    user.set_attributes(app.current_request.json_body)
    user.save()
    return user.to_json()


# Update an user object
@app.route('/users/{id}', methods=['DELETE'])
def delete_user(id):
    # Validate input id is valid
    try:
        user = User.get(id)
    except:
        raise NotFoundError("This id was not found in our system")

    user.delete()
    return Response( body=None, status_code=204 )
