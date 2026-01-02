def verify_password(plain_password, stored_password):
    return plain_password == stored_password

def get_password_hash(password):
    return password