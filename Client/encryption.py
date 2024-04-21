import base64

def encrypt(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    encoded_password = encoded_bytes.decode('utf-8')
    return encoded_password

def decrypt(password):
    decoded_bytes = base64.b64decode(password.encode('utf-8'))
    decoded_password = decoded_bytes.decode('utf-8')
    return decoded_password