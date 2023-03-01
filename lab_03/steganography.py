import streamlit as st
import numpy as np
import requests
import cv2

from PIL import Image, ImageDraw, UnidentifiedImageError
from urllib.parse import urlparse

from io import BytesIO


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


def to_bin(data):
    #convert data to binary format
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes):
        return ''.join([format(i, "08b") for i in data])
    elif isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encrypt(image_name, secret_data):
    # read the image
    image = cv2.imread(image_name)

    #maximum bytes to encode
    n_bytes = image.shape[0] * image[1] * 3 // 8

    st.markdown("[*] maximum bytes to encode:", n_bytes)

    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    st.markdown("Encoding data ...")

    # add stopping criteria
    secret_data += "====="
    data_index = 0

    # convert data to binary
    binary_secret_data = to_bin(secret_data)

    #size of data to hide
    data_len = len(binary_secret_data)

    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)






def main():
    st.markdown("## Laboratory work №3")
    st.markdown("### **Title**: Steganography")
    st.markdown("---")

    user_img = uploader(st.file_uploader("Upload your image", type=FILE_TYPES))
    user_url = validate_url(st.text_input(f"Inpute your image url {FILE_TYPES}: ", URL))

    img = get_image(user_img, user_url)

    message = st.text_area(
        "Input your message to be encrypted:",
        value="This is my first attempt to steganography!"
    )

    with st.form("encrypt"):
        st.form_submit_button("Encrypt")
        encrypted_img = encrypt(img, message)

    get_image_download_link(encrypted_img, "Save your image with encryption")

    with st.form("decrypt"):
        st.form_submit_button("Descrypt")
        decrypt(encrypted_img)


if __name__ == "__main__":
    main()
