from models.User import User

if User.exists():
    print("User table already exists...")
    User.delete_table()
User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

print("Adding User to the table...")
user = User(email="test@test.com")
user.save()

print("Adding User2 to the table...")
user = User(email="test2@test2.com")
user.save()

print("Selecting User from User Table by ID")
stored_user = User.get(user.id)
print(stored_user)

print("Selecting User from User Table by email")
stored_user = User.getByIndex('email', 'test@test.com')
print(stored_user)

print("Scanning users from User Table...")
for user in User.scan(User.email == "test@test.com"):
    print("Found")
    print(user)

print("Exiting...")

