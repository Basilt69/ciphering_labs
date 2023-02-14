import string
import pandas as pd
import streamlit as st


def caesar_ciphering(data, key):
    alphabet_lower = string.ascii_lowercase
    alphabet_upper = string.ascii_uppercase
    punctuation = string.punctuation

    ciphered_list = []

    st.markdown("**This is alphabet to check out the result:**")
    st.write(alphabet_lower)

    st.markdown("**This is punctuation that can be used**")
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


def caesar_deciphering(deciphering_msg, key_desc):
    alphabet_lower = string.ascii_lowercase
    alphabet_upper = string.ascii_uppercase
    punctuation = string.punctuation

    deciphered_list = []
    for letter in deciphering_msg:
        if letter.islower():
            try:
                deciphered_list.append(alphabet_lower[alphabet_lower.index(letter)-key_desc])
            except IndexError:
                deciphered_list.append(alphabet_lower[26 - abs(key_desc - alphabet_lower.index(letter))])
        elif letter.isupper():
            try:
                deciphered_list.append(alphabet_upper[alphabet_upper.index(letter)-key_desc])
            except IndexError:
                deciphered_list.append(alphabet_upper[26 - abs(key_desc-alphabet_upper.index(letter))])
        elif letter in punctuation:
            try:
                deciphered_list.append(punctuation[punctuation.index(letter) - key_desc])
            except IndexError:
                deciphered_list.append(punctuation[32 - abs(key_desc - punctuation.index(letter))])
        elif letter.isspace():
            deciphered_list.append(letter)
        elif letter.isnumeric():
            deciphered_list.append(str(int(letter) - key_desc))

    return ''.join(deciphered_list)


#cache the dataframe so it's only loaded once
@st.cache_data
def load_data():
    alphabet_lower = string.ascii_lowercase
    alphabet_upper = string.ascii_uppercase

    df_upper = pd.DataFrame()
    df_lower = pd.DataFrame()

    for i in range(26):
        df_upper[i] = alphabet_upper[i:] + alphabet_upper[:i]
        df_lower[i] = alphabet_lower[i:] + alphabet_lower[:i]

    return df_upper, df_lower





def main():
    st.markdown("## Laboratory work №1")
    st.markdown("### **Title**: Caesar and Vigenère ciphering")

    description_ces = """
    In cryptography, a Caesar cipher, also known as Caesar's cipher, the shift cipher, Caesar's code or Caesar shift, is
     one of the simplest and most widely known encryption techniques. It is a type of substitution cipher in which each
      letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet. For example, 
      with a left shift of 3, D would be replaced by A, E would become B, and so on. The method is named after Julius 
      Caesar, who used it in his private correspondence.
    """

    description_vig = """
    In a Caesar cipher, each letter of the alphabet is shifted along some number of places. For example, in a Caesar 
    cipher of shift 3, a would become D, b would become E, y would become B and so on. The Vigenère cipher has several 
    Caesar ciphers in sequence with different shift values. To encrypt, a table of alphabets can be used, termed a 
    tabula recta, Vigenère square or Vigenère table. It has the alphabet written out 26 times in different rows, each 
    alphabet shifted cyclically to the left compared to the previous alphabet, corresponding to the 26 possible Caesar 
    ciphers. At different points in the encryption process, the cipher uses a different alphabet from one of the rows. 
    The alphabet used at each point depends on a repeating keyword.
    """



    ciph_type = st.radio(
        "Choose ciphering type", (
            "1. Caesar ciphering",
            "2. Vigenère ciphering",
        )
    )

    if ciph_type[:1] == "1":
        show_schema = st.checkbox("Show description:")
        if show_schema:
            st.code(description_ces)

        st.markdown("**Please, input your text**")
        message = st.text_input("(All your text, punctuation and numbers will be shifted)")

        st.markdown('**Please, input your key(actual shift)**')
        key = st.number_input("(numbers shall be integers from 1 to 26)", min_value=0, max_value=26, step=1, value=1)

        st.markdown ("**This is our initial message:**")
        st.write(message)

        st.write("---")

        ciphered_msg = caesar_ciphering(message, key)

        st.markdown("**This is our ciphered message(using Caesar cipher):**")
        st.write(ciphered_msg)

        st.markdown("**Please, input your text to decipher**")
        deciphering_msg = st.text_input("(All your text, punctuation and numbers shall be shifted)")

        st.markdown('**Please, input your key(actual shift)**')
        key_desc = st.number_input("(numbers must be integers from 1 to 26)", min_value=0, max_value=26, step=1,
                                   value=1)

        deciphered_msg = caesar_deciphering(deciphering_msg, key_desc)
        st.markdown("**This is our deciphered message(using Caesar cipher):**")
        st.write(deciphered_msg)
    elif ciph_type[:1] == "2":
        show_schema = st.checkbox("Show description:")
        if show_schema:
            st.code(description_vig)

        st.markdown("**Please, input your text**")
        message = st.text_input("(Your text will be shifted irrespective of whether it is lower- or uppercase written)")

        st.markdown('**Please, input your key(word)**')
        key = st.text_input("(only english alphabet letters are allowed)")

        st.markdown("**This is our initial message:**")
        st.write(message)

        st.write("---")

        # Boolean to resize the dataframe, stored as a session state variable
        st.checkbox("Use container width", value=False, key="use_container_width")

        df_upper, df_lower = load_data()

        #display the dataframe and allow the user to stretch the dataframe
        #across the full width of the container, based on the checkbox value
        st.dataframe(df_upper, use_container_width=st.session_state.use_container_width)
        st.dataframe(df_lower, use_container_width=st.session_state.use_container_width)







if __name__ == "__name__":
    main()


