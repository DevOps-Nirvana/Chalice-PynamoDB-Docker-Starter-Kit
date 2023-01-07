from chalice import BadRequestError, NotFoundError
from pynamodb.models import Model
from pynamodb.util import attribute_value_to_json
import helpers
import models
import json


class BaseModel( Model ):
    """
    Provides base model for PynamoDB models, offering the following features:
      * A simple "print" helper for development/debugging
      * A classmethod modelClass helper for getting the child model or model name automatically
      * A classmethod helper to create from a dictionary automatically, respecting private/require fields (eg: for POST via REST endpoint)
      * A classmethod helper to search through a GSI (GlobalSecondaryIndex) on this model
      * A classmethod helper to scan through the table and return all results with a field having a value (aka, manual scan)
      * A helper to set attributes based on an input dict (with input validation)
    """
    # class Meta:
    #     host = helpers.get_dynamodb_endpoint()
    #     required_fields  = []
    #     read_only_fields = ["id"]
    #     validate_fields  = {}


    def __repr__(self):
        """
        Simple "print" object helper
        """
        return "{}({})".format(self.__class__, self.id)
        # return "{}({}): {}".format(__class__, self.id, self.to_json())


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
    def getByIndex(self, field_name, search_query, max_results=1):
        """
        Class method helper to search this model for a record automatically by an indexed field (via an GlobalSecondaryIndex)
        """
        # Try to get the field name's index if we can
        try:
            model_class = self.getModelClass()
            index_to_search = getattr(model_class, f"{field_name}_index")
        except AttributeError as e:
            raise AttributeError(f"Field {field_name} does not have an index")

        # Trying to search through this index, returning a single value if requested (default) otherwise a list view
        # if singular requested and failed, raises exception
        output = []
        for item in index_to_search.query(search_query, page_size=max_results):
            output.append(item)
        if max_results == 1:
            if len(output) >= 1:
                return output[0]
            raise NotFoundError({'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Not Found'}}, "getByIndex")
        return output


    def set_attributes(self, dict) -> None:
        """
        Simple update/set-attributes helper, validating fields as we go
        """
        for key in dict:
            # If we wish to validate fields
            if hasattr(self.Meta, "validate_fields"):
                if key in self.Meta.validate_fields:
                    validator = self.Meta.validate_fields[key]
                    if not validator(dict[key]):
                        raise BadRequestError(f'Field has invalid syntax/value: {key}')
            # If we have a setter helper
            if hasattr(self, f"set_{key}"):
                setter = getattr(self, f"set_{key}")
                setter(dict[key])
            else:
                # Otherwise just set the value
                self.attribute_values[key] = dict[key]


    def to_dict_safe(self) -> str:
        """
        Simple output helper, but only the desired fields to serialize
        """
        # If we only want specific fields, use our conditional
        if hasattr(self.Meta, "serialized_fields"):
            # Original, copied from PynamoDB/models.py:1141 (to_json(self)), just added conditional
            return {k: attribute_value_to_json(v) for k, v in self.serialize().items() if k in self.Meta.serialized_fields}
        # Otherwise, use our default serializer
        return {k: attribute_value_to_json(v) for k, v in self.serialize().items()}



    def to_json_safe(self) -> str:
        """
        Simple output helper, but only the desired fields to serialize
        """
        # If we only want specific fields, use our conditional
        if hasattr(self.Meta, "serialized_fields"):
            # Original, copied from PynamoDB/models.py:1141 (to_json(self)), just added conditional
            return json.dumps({k: attribute_value_to_json(v) for k, v in self.serialize().items() if k in self.Meta.serialized_fields})
        # Otherwise, use our default serializer
        return self.to_json()


    @classmethod
    def getByField(self, field_name, search_query, max_results=1):
        # Try to get the field name's index if we can
        try:
            model_class = self.getModelClass()
            field_to_search = getattr(model_class, field_name)
        except AttributeError as e:
            raise AttributeError(f"Field {field_name} does not exist")

        # Trying to search through this index, returning a single value if requested (default) otherwise a list view
        # if singular requested and failed, raises exception
        output = []
        for item in model_class.scan(field_to_search.contains(search_query), page_size=max_results):
            output.append(item)
        if max_results == 1:
            if len(output) >= 1:
                return output[0]
            raise NotFoundError({'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Not Found'}}, "getByField")
        return output
