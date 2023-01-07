from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BinaryAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection, AllProjection
from .BaseModel import BaseModel
import helpers
import hmac
import os


class UserEmailIndex( GlobalSecondaryIndex ):
    """
    This class represents a index on the email field
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        host = helpers.get_dynamodb_endpoint()
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    # This attribute is the hash key for the index
    email = UnicodeAttribute(hash_key=True)


class User( BaseModel ):
    """
    This class represents our User object/model
    """
    class Meta:
        table_name = "{}__User".format(helpers.get_stage())
        host = helpers.get_dynamodb_endpoint()  # This gets our dynamodb endpoint both locally during development and inside AWS Lambda
        region = helpers.get_deployed_region()
        required_fields  = ["email", "password", "name"]
        validate_fields  = {
            "email": helpers.validateEmail,
        }
        # Only output certain fields
        serialized_fields = ['id', 'email', 'name']

    id            = UnicodeAttribute(hash_key=True, default=helpers.getUUID)
    email         = UnicodeAttribute()
    email_index   = UserEmailIndex()
    password      = BinaryAttribute()
    password_salt = BinaryAttribute()
    name          = UnicodeAttribute()


    # Set the password and password salt on this object
    def set_password(self, password):
        self.password_salt, self.password = helpers.hash_password(password)


    # Validate an input password
    def verify_password(self, password):
        try:
            test_salt, test_hash = helpers.hash_password(password, self.password_salt)
            if hmac.compare_digest(test_hash, self.password):
                return True
        except:
            pass
        return False
