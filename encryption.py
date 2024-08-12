from cryptography.fernet import Fernet

class Encryption:
    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()  # Generate a new key if not provided
        self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext):
        return self.cipher.encrypt(plaintext.encode()).decode()  # Encode to string

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext.encode()).decode()  # Decode from string

    def get_key(self):
        return self.key.decode()  # Return the key as a string

# Example Usage:
# encryption = Encryption()
# encrypted_password = encryption.encrypt("my_secret_password")
# decrypted_password = encryption.decrypt(encrypted_password)