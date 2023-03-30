import streamlit as st
import sympy

from random import randint

'''
Source: https://cryptor.net/bezopasnost/diffie-hellman-protocol?ysclid=lfuy73fi8f479041113

Wiki: https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
'''


class DH_Endpoint(object):
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None

    def generate_partial_key(self):
        partial_key = self.public_key1**self.private_key
        partial_key = partial_key%self.public_key2
        return partial_key

    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r**self.private_key
        full_key = full_key%self.public_key2
        self.full_key = full_key
        return full_key

    def encrypt_message(self, message):
        encrypted_message = ""
        key = self.full_key
        for c in message:
            encrypted_message += chr(ord(c) + key)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c) - key)
        return decrypted_message


# public key - primes generation
def pub_keys_gen():
    p = sympy.randprime(0,100)
    g = p * randint(1,100) + 1
    #wiki says that p shall be just prime
    '''if sympy.isprime((p-1)/2):
        return p, 1%p #return p and g(mod p) which are public keys
    else:
        pub_keys_gen()
    return p, 1 % p'''
    return p, g # return p and g(mod p) which are public keys


# private key - primes generation
def priv_keys_gen():
    return sympy.randprime(0,100), sympy.randprime(0,100)


def encryption(message):
    #generation of keys
    public_key1, public_key2 = pub_keys_gen()
    st.write("This is public key #1: ", public_key1)
    st.write("This is public key #2: ", public_key2)

    private_key1, private_key2 = priv_keys_gen()
    st.write("This is private key #1: ", private_key1)
    st.write("This is private key #2: ", private_key2)


    # creation of users
    Alice = DH_Endpoint(public_key1, public_key2, private_key1)
    Bob = DH_Endpoint(public_key1, public_key2, private_key2)

    a_partial = Alice.generate_partial_key()
    b_partial = Bob.generate_partial_key()
    st.write("This is Alice's partial key: ", a_partial)
    st.write("This is Bob's partial key: ", b_partial)

    a_full = Alice.generate_full_key(b_partial)
    b_full = Bob.generate_full_key(a_partial)
    st.write("This is Alice's full key: ", a_full)
    st.write("This is Bob's full key: ", b_full)

    msg_encrypted = Alice.encrypt_message(message)

    return msg_encrypted, Bob


#decryption of the encrypted message
def decryption(ciphertext, Bob):
    message = Bob.decrypt_message(ciphertext)
    return message


def main():
    st.markdown("## Laboratory work №5")
    st.markdown("### **Title**: Diffie-Hellman algorithm (key exchange)")
    st.markdown("---")

    st.markdown("""Diffie–Hellman key exchange is a mathematical method of securely exchanging cryptographic keys 
    over a public channel and was one of the first public-key protocols as conceived by Ralph Merkle and named after 
    Whitfield Diffie and Martin Hellman. DH is one of the earliest practical examples of public key exchange 
    implemented within the field of cryptography. Published in 1976 by Diffie and Hellman, this is the earliest publicly
    known work that proposed the idea of a private key and a corresponding public key.""")
    st.markdown("---")

    with st.form('diffie-hellman encoding'):
        message = st.text_area(
            "**Please, input your text to be send**",
            value="Never say never!"
        )


        '''public_key1 = st.number_input(
            "**Please, input your public key(integer)**",
            value=197
        )

        public_key2 = st.number_input(
            "**Please, input your public key(integer)**",
            value=151
        )

        private_key1 = st.number_input(
            "**Please, input your private key(integer)**",
            value=199
        )
        private_key2 = st.number_input(
            "**Please, input your private key(integer)**",
            value=157
        )'''

        st.form_submit_button("Encrypt")
        ciphertext, receiver = encryption(message)
        st.write("Encryption result:")
        st.code(ciphertext)


    with st.form("diffie-hellman decoding"):
        st.form_submit_button("Decryption")
        decrypted = decryption(ciphertext, receiver)
        st.write(decrypted)


if __name__ == "__main__":
    main()