import string
import streamlit as st


def caesar_ciphering(data, key):
    alphabet_lower = string.ascii_lowercase
    alphabet_upper = string.ascii_uppercase
    punctuation = string.punctuation

    ciphered_list = []

    st.markdown("### This is alphabet to check out the result:")
    st.write(alphabet_lower)

    st.markdown("### This is punctuation that can be used")
    st.write(punctuation)

    for letter in data:
        if letter.islower():
            try:
                ciphered_list.append(alphabet_lower[alphabet_lower.index(letter)+key])
            except IndexError:
                ciphered_list.append(alphabet_lower[key - (26 - alphabet_lower.index(letter))])
        elif letter.isupper():
            try:
                ciphered_list.append(alphabet_upper[alphabet_upper.index(letter)+key])
            except IndexError:
                ciphered_list.append(alphabet_upper[key - (26 - alphabet_upper.index(letter))])
        elif letter in punctuation:
            try:
                ciphered_list.append(punctuation[punctuation.index(letter) + key])
            except IndexError:
                ciphered_list.append(punctuation[key - (32 - punctuation.index(letter))])
        elif letter.isspace():
            ciphered_list.append(letter)
        elif letter.isnumeric():
            ciphered_list.append(str(int(letter) + key))

    return ''.join(ciphered_list)


def main():
    st.markdown("## Laboratory work №1")
    st.markdown("**Title**: Caesar and Vigenère ciphering")

    st.markdown("### Please, input your text")
    message = st.text_input("(All your text, punctuation and numbers will be shifted)")

    st.markdown('### Please, input your key(actual shift)')
    key = st.number_input("(numbers shall be integers from 1 to 26)", min_value=0, max_value=26, step=1, value=1)

    st.markdown ("### This is our initial message:")
    st.write(message)

    st.write("---")

    ciphered_msg = caesar_ciphering(message, key)

    st.markdown("#### This is our ciphered message(using Caesar cipher):")
    st.write(ciphered_msg)
    st.markdown(
        """
        <style>
        input {
            font-size: 48px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



if __name__ == "__name__":
    main()


