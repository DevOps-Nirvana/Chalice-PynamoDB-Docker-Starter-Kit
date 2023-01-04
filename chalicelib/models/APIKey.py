from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BinaryAttribute, TTLAttribute, JSONAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection, AllProjection
from botocore.client import ClientError
from .BaseModel import BaseModel
import helpers


class APIKey( BaseModel ):
    """
    This class represents our APIKey object/model
    """
    class Meta:
        table_name = "{}__APIKey".format(helpers.get_stage())
        host = helpers.get_dynamodb_endpoint()  # This gets our dynamodb endpoint both locally during development and inside AWS Lambda
        region = helpers.get_deployed_region()

    id      = UnicodeAttribute(hash_key=True, default=helpers.getDoubleUUID)
    ttl     = TTLAttribute(default=helpers.getTTLExpiration)
    user_id = UnicodeAttribute(null=False)
    label   = UnicodeAttribute(null=False)
