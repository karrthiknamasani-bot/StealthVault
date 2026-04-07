from cryptography.fernet import Fernet
from PIL import Image

DELIMITER = "#####"


# ---------- ENCRYPTION ----------

def generate_key():
    return Fernet.generate_key()


def encrypt_message(message, key):
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())


def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message).decode()


# ---------- STEGANOGRAPHY ----------

def encode_image(image_path, data):
    img = Image.open(image_path)

    # 🔥 FORCE RGB (handles ALL formats)
    img = img.convert("RGB")

    pixels = img.load()

    # Convert data to binary + delimiter
    binary_data = ''.join(format(byte, '08b') for byte in data)
    binary_data += ''.join(format(ord(i), '08b') for i in DELIMITER)

    index = 0

    for y in range(img.height):
        for x in range(img.width):
            if index < len(binary_data):
                r, g, b = pixels[x, y]

                r = (r & ~1) | int(binary_data[index])
                index += 1

                if index < len(binary_data):
                    g = (g & ~1) | int(binary_data[index])
                    index += 1

                if index < len(binary_data):
                    b = (b & ~1) | int(binary_data[index])
                    index += 1

                pixels[x, y] = (r, g, b)

    output_path = "stego.png"
    img.save(output_path)
    return output_path


def decode_image(image_path):
    img = Image.open(image_path)

    # 🔥 FORCE RGB
    img = img.convert("RGB")

    pixels = img.load()

    binary_data = ""

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]

            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded = ""

    for byte in bytes_data:
        decoded += chr(int(byte, 2))
        if decoded.endswith(DELIMITER):
            break

    return decoded[:-len(DELIMITER)].encode()