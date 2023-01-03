from models.User import User
from models.APIKey import APIKey

print("Adding User to the table...")
user = User(email="test@test.com", name="tester1")
user.set_attributes({'password': 'test'})
user.save()
print(user)

print("Adding User2 to the table...")
user2 = User(email="test2@test.com", name="tester2")
user2.set_attributes({'password': 'test'})
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

