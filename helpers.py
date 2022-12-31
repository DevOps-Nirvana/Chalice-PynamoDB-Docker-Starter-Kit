# For regex, for checking email validation
import re
# For UUID to generate uuids easily and automatically for objects
from uuid import uuid4


# Simple auto-uuid helper for setting on model ID fields
def getUUID():
    return str(uuid4())


# Simple email syntax validation
def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False
