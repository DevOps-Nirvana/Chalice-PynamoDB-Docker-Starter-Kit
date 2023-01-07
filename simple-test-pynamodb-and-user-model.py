import sys

# This injects our chalicelib folder as a path to include from automatically
sys.path.insert(0,'chalicelib')

from models.User import User
from models.APIKey import APIKey

print("Adding user...")
user = User.createFromDict({'email': 'test@test.com', 'name': 'tester1', 'password': 'test'})
user.save()
print(user)

print("Adding user2...")
user2 = User.createFromDict({'email': 'test2@test.com', 'name': 'tester2', 'password': 'test'})
user2.save()
print(user2)

print("Selecting User from User Table by ID")
print(user.id)
stored_user = User.get(user.id)
print(stored_user)

print("Selecting User from User Table by email")
print(user.email)
stored_user = User.getByIndex('email', user.email)
print(stored_user)

print("Scanning users from User Table...")
for stored_user in User.getByField('name', user2.name, max_results=100):
    print("Found {}".format(stored_user.id))

print("removing users...")
user.delete()
user2.delete()

print("Exiting...")

