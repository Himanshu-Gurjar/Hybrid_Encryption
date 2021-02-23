from Crypto.Cipher import AES
from Crypto import Random
from Cryptography import AES_key, RSA_keys
import zlib
import pathlib
import os
from getpass import getuser

block_size: int = 128  # size of a key

# Default path for storing the keys, encrypted file and decrypted file.
default_path = f"C:/Users/{getuser()}/Hybrid Encryption"


def get_file_name(file_path, extension=False):
    """Returns file name from given path
    either with extension or without extension

    :param file_path:
    :param extension:
    :return file_name:
    """
    if not extension:
        file_name = pathlib.Path(file_path).stem

    else:
        file_name = os.path.basename(file_path)

    return file_name


def str_to_bytes(value: [str, bytes]) -> bytes:

    if isinstance(value, str):
        return value.encode(encoding='utf8')
    return value


def get_magic() -> bytes:
    magic: bytes = str_to_bytes("HyBrIdEnCrYpTiOn")
    magic = zlib.compress(magic)
    return magic


def pad(string):
    """Returns the padded text for encryption"""

    return string + (block_size - len(string) % block_size) * str_to_bytes(
        chr(block_size - len(string) % block_size))


def unpad(string):
    """Unpad the text and then returns it for decryption"""

    return string[:-ord(string[len(string) - 1:])]


def is_file_encrypted(magic, file_contents):
    """Checks whether the file is already encrypted or not"""

    return file_contents[:len(magic)] == magic


def get_file_path(file_path):
    """Returns the file_path for storing the encrypted file"""

    file_name = os.path.basename(file_path)
    file_path = f"{default_path}/{file_name}.enc"
    return file_path


def encryption(file_path):
    """
    Read the given file in byte mode,
    get the AES key for encryption,
    pad the text,
    generate the random initialization vector(iv) of 16 bytes,
    mode for encryption : CBC,
    generate the cipher for encryption using AES key, Mode, Iv,
    using cipher encrypt the plaintext and then add the Iv to it and value stored in cipher_text,
    before writing the cipher text, write the magic text for determining whether the file is encrypted or not,
    then write the cipher text.
    returns the appropriate massage

    :param file_path:
    :return mgs:
    """

    if not RSA_keys.is_encryption_directory_exist():
        RSA_keys.create_encryption_directory()

    file_reader = open(file_path, "rb")
    plaintext = file_reader.read()
    file_reader.close()

    if is_file_encrypted(get_magic(), plaintext):
        mgs = "File is already encrypted cannot encrypt again"
        return mgs

    session_key = AES_key.get_key()
    raw_data = pad(plaintext)
    iv = Random.new().read(AES.block_size)
    mode = AES.MODE_CBC
    cipher = AES.new(session_key, mode, iv)
    cipher_text = iv + cipher.encrypt(raw_data)
    try:
        encrypted_file_path = get_file_path(file_path)
        with open(encrypted_file_path, "wb") as encrypted_file:
            encrypted_file.write(get_magic())
            encrypted_file.write(cipher_text)
            encrypted_file.close()
        mgs = f"File successfully encrypted & stored at :\n{default_path}"

    except Exception as e:
        mgs = "There is some error please check the selected file"
        print(e)

    return mgs


def decryption(file_path):
    """
    This function use for decryption,
    First it will check whether the keys are there or not,
    if keys are present then it will read the file and
    check whether it is encrypted or not,
    if the file is encrypted then decrypt it using AES key
    and returns appropriate massage
    :param file_path:
    :return mgs:
    """

    magic = get_magic()
    if not (RSA_keys.is_file_exist() and AES_key.is_AES_key_exist()):
        mgs = "Keys which are used for encryption either deleted or corrupted, Cannot Decrypt"
        return mgs

    try:

        with open(file_path, "rb") as encrypted_file:
            cipher_text = encrypted_file.read()
            encrypted_file.close()

        if not is_file_encrypted(magic, cipher_text):
            mgs = "Given file is not encrypted, please encrypt it first"
            return mgs

        cipher_text = cipher_text[len(magic):]
        session_key = AES_key.get_key()
        iv = cipher_text[:AES.block_size]
        mode = AES.MODE_CBC
        cipher = AES.new(session_key, mode, iv)
        plaintext = unpad(cipher.decrypt(cipher_text[AES.block_size:]))

        file_name = get_file_name(file_path)
        with open(f"{default_path}/{file_name}", "wb") as decrypted_file:
            decrypted_file.write(plaintext)
            decrypted_file.close()

        os.remove(file_path)   # Removes the encrypted file after completion of decryption
        mgs = f"File successfully decrypted & stored at :\n{default_path}"

    except Exception as e:
        mgs = "There is some error please check the selected file"
        print(e)

    return mgs
