# For imports/exceptions see: https://github.com/aws/chalice/blob/master/chalice/__init__.py
from chalice import ConflictError, NotFoundError, Response, ForbiddenError, UnauthorizedError, NotFoundError
import json

# Grabbing our models and our validate functions/helpers
from models.APIKey import APIKey
from models.User import User
from .internal__routes import validate_api_key
import helpers

# Grab our chalice app singleton object so we can define new APIs
app = helpers.get_chalice_app()


# Create an new user object
@app.route('/users', methods=['POST'])
def create_user():
    # Validate not a duplicate
    try:
        user = User.getByIndex('email', app.current_request.json_body['email'])
        raise NotFoundError('This email already exists in our system')
    except NotFoundError as e:
        if "ResourceNotFoundException" not in str(e):
            raise

    # Create the object via helper and return the results to the user with the right HTTP code
    return Response(
        body=User.createFromDict(app.current_request.json_body).to_json_safe(),
        status_code=201
    )


# Login with our email and password (and optionally expire_in_hours which is 24 by default)
@app.route('/login', methods=['POST'])
def login():
    try:
        user = User.getByIndex('email', app.current_request.json_body['email'])
    except:
        # Doing this here simulates the exact time it would take to hash the password to validate it.  This prevents
        # an attack vector knowing when emails are invalid because they would take less long to respond than if they were valid.
        user = User(email="invalid@invalid.com")
        user.set_password("invalid")
        raise UnauthorizedError("These credentials are invalid")
    try:
        if user.verify_password(app.current_request.json_body['password']):
            print("Adding APIKey for {}".format(user.id))
            api_key = APIKey(user_id=user.id)
            if 'expire_in_hours' in app.current_request.json_body:
                api_key.ttl = helpers.getTTLExpiration(app.current_request.json_body['expire_in_hours'])
            api_key.label = "via login"
            api_key.save()
            return api_key.to_json_safe()
    except Exception as e:
        print("An unexpected exception occurred")
        print(e)
        raise UnauthorizedError("These credentials are invalid")


# Get an user object
@app.route('/users/{id}', methods=['GET'], authorizer=validate_api_key)
def get_user(id):
    # Validate input id is valid
    try:
        user = User.get(id)
    except:
        raise NotFoundError("This id was not found in our system")

    # Load our principal (Json encoded user)
    principal = json.loads(app.current_request.context['authorizer']['principalId'])

    # Check if it's us we are querying
    if user.id != principal['id']:
        raise ForbiddenError("You do not have permissions to use this")

    return user.to_json_safe()


# List all user objects (TODO: Does not support pagination)
@app.route('/users', methods=['GET'], authorizer=validate_api_key)
def list_user():
    output = []
    for item in User.scan():
        row = item.to_dict_safe()
        del row['email']  # Email is sensitive, lets strip it here for now, until we make something better in the BaseModel for private fields
        output.append(row)
    return json.dumps(output)


# Update an user object
@app.route('/users/{id}', methods=['PUT', 'PATCH'], authorizer=validate_api_key)
def update_user(id):
    # Validate input id is valid
    try:
        user = User.get(id)
    except:
        # We should use Forbidden for more security, but we could use NotFound
        raise ForbiddenError("You do not have permissions to use this")
        # raise NotFoundError("This id was not found in our system")

    # Load our principal (Json encoded user)
    principal = json.loads(app.current_request.context['authorizer']['principalId'])

    # Check if it's us we are updating
    if user.id != principal['id']:
        raise ForbiddenError("You do not have permissions to use this")

    # Update attributes
    user.set_attributes(app.current_request.json_body)
    user.save()
    return user.to_json_safe()


# Delete an user object
@app.route('/users/{id}', methods=['DELETE'], authorizer=validate_api_key)
def delete_user(id):
    # Validate input id is valid
    try:
        user = User.get(id)
    except:
        # We should use Forbidden for more security, but we could use NotFound
        raise ForbiddenError("You do not have permissions to use this")
        # raise NotFoundError("This id was not found in our system")

    # Load our principal (Json encoded user)
    principal = json.loads(app.current_request.context['authorizer']['principalId'])

    # Check if it's us we are deleting
    if user.id != principal['id']:
        raise ForbiddenError("You do not have permissions to use this")

    # TODO: Should consider also deleting all (soft) FK'd resources (eg: API Keys)
    print("Preparing to delete user, grabbing all API Keys...")
    for api_key in APIKey.getByField('user_id', user.id, max_results=1000):
        print("Deleting APIKey: {}".format(api_key.id))
        api_key.delete()

    print("Deleting user {}".format(user.id))
    user.delete()
    return Response( body=None, status_code=204 )


# Tells you who you are
@app.route('/whoami', methods=['GET'], authorizer=validate_api_key)
def whoami():
    return app.current_request.context['authorizer']['principalId']
