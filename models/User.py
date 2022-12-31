from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from botocore.client import ClientError
from .BaseModel import BaseModel
import helpers


class UserEmailIndex( GlobalSecondaryIndex ):
    """
    This class represents a index on the email field
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        read_capacity_units = 1
        write_capacity_units = 1
        projection = KeysOnlyProjection()

    # This attribute is the hash key for the index
    email = UnicodeAttribute(hash_key=True)


class User( BaseModel ):
    """
    This class represents our User object/model
    """
    class Meta:
        table_name = 'User'
        host = "http://dynamodb:8000"
        required_fields  = ["email"]
        read_only_fields = ["id"]
        validate_fields  = {
            "email": helpers.validateEmail,
        }

    id          = UnicodeAttribute(hash_key=True, default=helpers.getUUID)
    email       = UnicodeAttribute()
    email_index = UserEmailIndex()
