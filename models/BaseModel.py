from chalice import BadRequestError
from botocore.client import ClientError
from pynamodb.models import Model
import models


class BaseModel( Model ):
    """
    Provides base model for PynamoDB models, offering the following features:
      * A simple "print" helper for development/debugging
      * A modelClass helper for getting the child model automatically
      * A helper to create from a dictionary automatically, respecting private/require fields
      * A helper to set attributes based on an input dict (no validation)
    """

    def __repr__(self):
        """
        Simple "print" object helper
        """
        return "{}({}): {}".format(__class__, self.id, self.to_json())


    @classmethod
    def getModelName(self):
        """
        Allows us to get the model name
        """
        return self.__name__


    @classmethod
    def getModelClass(self):
        """
        Allows us to get the model class of the children model, not of the parent allowing us to
        perform helpers like the createFromDict below automatically using the proper child class
        """
        return getattr(models, self.__name__)


    @classmethod
    def createFromDict(self, dict):
        """
        Create from a dictionary automatically, respecting private/require fields (eg: via REST)
        """
        model_class = self.getModelClass()

        # Validate required field(s), if present
        if hasattr(model_class.Meta, "required_fields"):
            for item in model_class.Meta.required_fields:
                if item not in dict:
                    raise BadRequestError(f'Missing field: {item}')

        # Validate if trying to set private field(s), if present
        if hasattr(model_class.Meta, "read_only_fields"):
            for item in model_class.Meta.read_only_fields:
                if item in dict:
                    raise BadRequestError(f'Unable to set private field: {item}')

        # Create object, set our attributes and save it
        new_object = model_class()
        new_object.set_attributes(dict)
        new_object.save()

        return new_object


    @classmethod
    def getByIndex(self, field_name, search_query):
        """
        Class method helper to search this model for a record automatically by an indexed field (via an GlobalSecondaryIndex)
        """
        # Try to get the field name's index if we can
        try:
            model_class = self.getModelClass()
            index_to_search = getattr(model_class, f"{field_name}_index")
        except AttributeError as e:
            raise AttributeError(f"Field {field_name} does not have an index")

        # Trying to search through this index, returning the first valid value
        for item in index_to_search.query(search_query):
            return item
        raise ClientError({'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Not Found'}}, "getByIndex")


    def set_attributes(self, dict):
        """
        Simple update/set-attributes helper, validating fields as we go
        """
        for key in dict:
            if hasattr(self.Meta, "validate_fields"):
                if key in self.Meta.validate_fields:
                    validator = self.Meta.validate_fields[key]
                    if not validator(dict[key]):
                        raise BadRequestError(f'Field has invalid syntax/value: {key}')
            self.attribute_values[key] = dict[key]
