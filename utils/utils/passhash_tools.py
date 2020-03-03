import bcrypt
def get_passhash(password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(password, bcrypt.gensalt())

def check_password(password, passhash):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(password, passhash)