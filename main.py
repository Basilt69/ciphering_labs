import streamlit as st

from lab_01 import caesar_ciphering


st.sidebar.image('logo.png', width=300)


def header():
    author = """
        made by [Basil Tkachenko](https://github.com/Basilt69)
        for **Ciphering labs**
        in [BMSTU](https://bmstu.ru) 
    """

    st.header("BMSTU, University cathedra: Informatics and software management - 7")
    st.markdown("**Course title:** Data protection")
    st.markdown("University lecturer: Kivva K.A.")
    st.markdown("**Student:** Tkachenko B.M.")
    st.sidebar.markdown(author)

def main():
    header()
    lab = st.sidebar.radio(
        "Select your lab:", (
            "1. Caesar and Vigenère cipher",
        ),
        index=2
    )

    if lab[:1] == "1":
        message = st.text_input("Please, input your text")
        key = st.number_input('Please, input your key(actual shift)')
        st.write("This our initial message:", message)

        ciphered_message = caesar_ciphering.caesar_ciphering(message, key)
        st.write("This is what we've got as the result of ciphering:", ciphered_message)

if __name__ == "__main__":
    main()

