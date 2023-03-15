import streamlit as st
import numpy as np
import requests
import cv2

from PIL import Image, ImageDraw, UnidentifiedImageError
from urllib.parse import urlparse
from random import randint
from io import BytesIO

from io import BytesIO

#kdmg
FILE_TYPES = ["png", "bmp"]

URL = "https://adonius.club/uploads/posts/2022-01/1641932928_8-adonius-club-p-fon-gor-8.png"


def get_image_download_link(img, label="Save image"):
    img.save("img.png")
    with open("img.png", "rb") as file:
        return st.download_button(
            label=label,
            data=file,
            file_name="ciphering_lab.png",
            mime="image/png"
        )


def uploader(file):
    show_file = st.empty()
    if not file:
        show_file.info("valid file extension: " + ", ".join(FILE_TYPES))
        return False
    return file


def not_valid_url_err():
    return st.error("Seems like you've inputed not url. Try again please!")


def validate_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
        elif not url:
            not_valid_url_err()
            return False
        else:
            not_valid_url_err()
            return False
    except AttributeError:
        not_valid_url_err()
        return False


def get_image(user_img, user_url):
    img = None
    if user_img is not False:
        img = Image.open(user_img)
    else:
        response = requests.get(user_url)
        try:
            img = Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            st.write("Something went wrong... try again!")
            st.stop()
    st.image(img)
    get_image_download_link(img)
    return img


def encrypt_2(img, message):
    keys = []
    draw_object = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    pixels = img.load()

    for elem in ([ord(elem) for elem in message]):
        key = (randint(1, width - 10), randint(1, height - 10))
        g, b = pixels[key][1:3]
        draw_object.point(key, (elem, g, b))
        keys.append(key)

    st.write("Keys:")
    st.code(keys)
    st.write("Image with an encrypted text:")
    st.image(img)
    return keys, img


def decrypt_2(img, keys):
    a = []
    pixels = img.load()
    for key in keys:
        a.append(pixels[key][0])
    res = ''.join([chr(elem) for elem in a])
    st.write(res)


def main():
    st.markdown("## Laboratory work №3")
    st.markdown("### **Title**: Steganography")
    st.markdown("---")

    user_img = uploader(st.file_uploader("Upload your image", type=FILE_TYPES))
    user_url = validate_url(st.text_input(f"Input your image url {FILE_TYPES}: ", URL))

    img = get_image(user_img, user_url)

    message = st.text_area(
        "Input your message to be encrypted:",
        value="This is my first attempt to steganography!"
    )

    with st.form("encrypt"):
        st.form_submit_button("Encrypt")
        keys, encrypted_img = encrypt_2(img, message)

    get_image_download_link(encrypted_img, "Save your image with encryption")

    with st.form("decrypt"):
        st.form_submit_button("Descrypt")
        decrypt_2(encrypted_img, keys)


if __name__ == "__main__":
    main()
