import streamlit as st
from main import *
from PIL import Image

st.title("🔐 StealthVault")

option = st.selectbox("Choose Action", ["Encrypt & Hide", "Extract & Decrypt"])


# ---------- ENCRYPT ----------
if option == "Encrypt & Hide":
    message = st.text_area("Enter Secret Message")
    image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if st.button("Encrypt & Embed"):
        if message and image:
            key = generate_key()
            encrypted = encrypt_message(message, key)

            # 🔥 Convert uploaded image safely
            img = Image.open(image)
            img = img.convert("RGB")
            img.save("temp.png")

            output = encode_image("temp.png", encrypted)

            st.success("Message hidden successfully!")
            st.image(output)

            st.download_button("Download Stego Image", open(output, "rb"), "stego.png")

            st.text("⚠ Save this key carefully:")
            st.code(key.decode())


# ---------- DECRYPT ----------
elif option == "Extract & Decrypt":
    image = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"])
    key = st.text_input("Enter Decryption Key")

    if st.button("Extract & Decrypt"):
        if image and key:
            try:
                img = Image.open(image)
                img = img.convert("RGB")
                img.save("temp.png")

                extracted = decode_image("temp.png")
                message = decrypt_message(extracted, key.encode())

                st.success("Hidden Message:")
                st.write(message)

            except:
                st.error("Invalid key or corrupted image")