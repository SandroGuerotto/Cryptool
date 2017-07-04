import os, random, struct, random, binascii
from Crypto.Cipher import AES


# Hier wird ein File entschlüsselt
def encrypt_file(key, in_filename, out_filename=None):
    if not out_filename:
        out_filename = in_filename + '.aes'
    else:
        array = in_filename.split("/")
        out_filename = out_filename + "/" + array[-1]

    with open(in_filename, 'rb') as infile:
        try:
            content = infile.read()
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(content)
            file_out = open(out_filename, "wb")
            [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
            return True
        except (TypeError, ValueError, AttributeError):
            return False


# Hier wird ein File verschlüsselt
def decrypt_file(key, in_filename, out_filename=None):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    else:
        array = in_filename.split("/")
        out_filename = out_filename + "/" + array[-1]

    with open(in_filename, 'rb') as infile:
        try:
            nonce, tag, ciphertext = [infile.read(x) for x in (16, 16, -1)]
            cipher = AES.new(key, AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)
        except (TypeError, ValueError, AttributeError):
            return False

        with open(out_filename, "wb") as outfile:
            outfile.write(data)
            outfile.close()
            return True


# Hier wird ein key importiert aus einem vorhandenen key file
def import_aeskey(path):
    if os.path.isfile(path):
        try:
            with open(path, 'r') as key_file:
                key = key_file.read()
                key_file.close()
                return key
        except (UnicodeDecodeError):
            return None
    return None


# Hier wird ein key in ein file exportiert
def save_key(key, path):
    path = path + "/AESkey.key"
    print(path)
    try:
        with open(path, "w") as key_file:
            key_file.write(key)
            key_file.close()
            return True
    except (UnicodeDecodeError):
        return False


# Hier wird ein neuer key erstellt mit 256 bit
def generate_new_key():
    return binascii.hexlify(os.urandom(16)).decode('utf-8')
