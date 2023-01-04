import os
import uuid
import time
import json
from optparse import OptionParser
import sys
sys.path.insert(0,'chalicelib')

# Models...
from models.User import User
from models.APIKey import APIKey

print("Starting migration script...")

# Note: Not really needed, but will keep incase someone wants to use env vars setting in config.json instead of dynamically generated table names
def record_as_env_var(key, value, stage):
    with open(os.path.join('.chalice', 'config.json')) as f:
        data = json.load(f)
        data['stages'].setdefault(stage, {}).setdefault(
            'environment_variables', {}
        )[key] = value
    with open(os.path.join('.chalice', 'config.json'), 'w') as f:
        serialized = json.dumps(data, indent=2, separators=(',', ': '))
        f.write(serialized + '\n')

if __name__ == '__main__':
    usage = "usage: %prog -s stage"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--stage",
                      dest="stage",
                      default="",
                      help="Name of the stage we are creating tables for",
                      metavar="stage-name")
    parser.add_option("-r", "--region",
                      dest="region",
                      help="The AWS Region we are creating in",
                      metavar="us-east-1")
    parser.add_option("-d", "--delete",
                      dest="delete",
                      action="store_true",
                      default=False,
                      help="If we want to delete the tables and re-create them, useful incase we change the schema")
    (options, args) = parser.parse_args()

    # Startup simple checks...
    if options.stage == "":
        print("ERROR: You MUST specify the stage with -s")
        parser.print_usage()
        exit(1)
    elif not options.region:
        print("ERROR: You MUST specify the region with -r")
        parser.print_usage()
        exit(1)
    os.environ["STAGE"] = options.stage


    # User table
    if User.exists():
        print("User table already exists, not running migrations")
        if options.delete:
            print("Deleting User table...")
            User.delete_table()
            print("Waiting for a few seconds to hopefully have the table delete...")
            time.sleep(10)
            print("Creating User table now...")
            User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
            record_as_env_var("USER_TABLE", User.Meta.table_name, options.stage)
    else:
        print("Creating User table now...")
        User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        record_as_env_var("USER_TABLE", User.Meta.table_name, options.stage)

    # APIKey table
    if APIKey.exists():
        print("APIKey table already exists, not running migrations")
        if options.delete:
            print("Deleting APIKey table...")
            APIKey.delete_table()
            print("Waiting for a few seconds to hopefully have the table delete...")
            time.sleep(10)
            print("Creating APIKey table now...")
            APIKey.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
            record_as_env_var("APIKEY_TABLE", APIKey.Meta.table_name, options.stage)
    else:
        print("Creating APIKey table now...")
        APIKey.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        record_as_env_var("APIKEY_TABLE", APIKey.Meta.table_name, options.stage)
