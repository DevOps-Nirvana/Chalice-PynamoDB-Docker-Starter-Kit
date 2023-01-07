from chalice import AuthResponse
from models.APIKey import APIKey
from models.User import User
import helpers

# Grab our chalice app singleton object so we can define new APIs
app = helpers.get_chalice_app()


# Our healthy endpoint, for health checks and such
@app.route('/healthy')
def healthy():
    return {'healthy': True}


# Authorizer validating API Key, cache for 300 seconds
@app.authorizer(ttl_seconds=300)
def validate_api_key(auth_request):
    try:
        # FOR DEBUGGING, UNCOMMENT IF NEEDED
        # print("Try to validate auth request...")
        # print(auth_request.method_arn)
        # print(auth_request.token)
        # print(auth_request)
        # print("Loading api key")
        api_key = APIKey.get(auth_request.token)
        # print(api_key)
        # print("Loading user")
        user = User.get(api_key.user_id)
        # print(user)
        # TODO: Set route paths according to user permissions, so it can be cached properly
        return AuthResponse(routes=['*'], principal_id=user.to_json())
    except Exception as e:
        print("Caught exception during authorizer")
        print(str(e))
        return AuthResponse(routes=[], principal_id='')
