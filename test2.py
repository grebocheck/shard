from users import User, get_user

new_user = User(user_id=11111111111,
                name="TEST1",
                username="@test1",
                phone_number="+38090000000",
                addres="my hard drive")
new_user.insert()
print(get_user(11111111111).username)
