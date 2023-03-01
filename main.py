import streamlit as st

from lab_01 import caesar_ciphering
from lab_02 import rsa
from lab_03 import steganography


st.sidebar.image('logo.png', width=300)


def header():
    author = """
        made by [Basil Tkachenko](https://github.com/Basilt69)
        for **Ciphering labs**
        in [BMSTU](https://bmstu.ru) 
    """

    st.header("BMSTU, University department: Informatics and software development - 7")
    st.markdown("**Course title:** Data protection")
    st.markdown("**University lecturer**: Kivva K.A.")
    st.markdown("**Student:** Tkachenko B.M.")
    st.sidebar.markdown(author)

def main():
    header()
    lab = st.sidebar.radio(
        "Select your lab:", (
            "1. Caesar and Vigenère cipher",
            "2. RSA ciphering",
            "3. Steganography ciphering",
        ),
        index=2
    )

    if lab[:1] == "1":
        caesar_ciphering.main()

    elif lab[:1] == "2":
        rsa.main()

    elif lab[:1] == "3":
        steganography.main()


if __name__ == "__main__":
    main()

