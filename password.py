from flask_bcrypt import Bcrypt
by=Bcrypt()
passa = by.generate_password_hash("shams").decode("utf-8")
print(by.check_password_hash(passa,'sham'))

