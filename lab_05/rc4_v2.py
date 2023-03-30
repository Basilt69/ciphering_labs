import streamlit as st
import codecs




def encryption(key, plain_text, n):
    #initial state vector array
    s = [i for i in range(0, 2**n)]
    st.write("Initial state vector array", s)

    key_list = [key[i:i + n] for i in range(0, len(key), n)]
    key_list = [bin(ord(i))[2:] for i in key_list]
    #st.write([ord(c) for c in key_list])
    #st.write([bin(ord(c))[2:] for c in key_list])

    # convert key_stream to decimal
    for i in range(len(key_list)):
        key_list[i] = int(key_list[i], 2)

    #convert plain_text to decimal
    pt = [plain_text[i:i + n] for i in range(0, len(plain_text), n)]

    for i in range(len(pt)):
        pt[i] = int(pt[i], 2)

    st.write('Plain text (in array form):', pt)

    # making key_stream equal to length of the state vector
    diff = int(len(s) - len(key_list))

    if diff != 0:
        for i in range(0, diff):
            key_list.append(key_list[i])
    st.write("Key list:", key_list)

    # perform KSA algorithm
    def KSA():
        j = 0
        N = len(s)

        #iterate over the range [0, N]
        for i in range(0, N):

            # find the key
            j = (j + s[i] + key_list[i]) % N
            #update s[i] and s[j]
            s[i], s[j] = s[j], s[i]
            st.write(s)

        initial_permutation_array = s
        st.write("The initial permutation array is:", initial_permutation_array)
        return initial_permutation_array

    st.write("KSA iterations:")

    initial_permutation_array = KSA()
    st.code(initial_permutation_array)

    #perform PGRA algorithm
    def PGRA():

        N = len(s)
        i = j = 0
        key_stream = []

        #iterate over [0, length of pt]
        for k in range(0, len(pt)):
            i = (i + 1) % N
            j = (j + s[i]) % N

            #update s[i] and s[j]
            s[i], s[j] = s[j], s[i]
            t = (s[i] + s[j]) % N
            key_stream.append(s[t])

        st.write("Key stream", key_stream)
        return key_stream

    key_stream = PGRA()


    # performing XOR between generated key stream and plain text
    def XOR():
        cipher_text = []
        for i in range(len(pt)):
            c = key_stream[i] ^ pt[i]
            cipher_text.append(c)
        return cipher_text

    cipher_text = XOR()

    # convert the encrypted text into bits form
    encrypted_to_bits = ""
    for i in cipher_text:
        encrypted_to_bits += '0'*(n-len(bin(i)[2:])) + bin(i)[2:]

    st.write(encrypted_to_bits)
    return encrypted_to_bits



def main():
    st.markdown("## Laboratory work №5")
    st.markdown("### **Title**: RC4 algorithm(stream cipher)")
    st.markdown("---")

    st.markdown("""**RC4 was designed by Ron Rivest of RSA Security in 1987. While it is officially termed "Rivest 
    Cipher 4", the RC acronym is alternatively understood to stand for Ron's Code. RC4 was initially a trade secret, 
    but in September 1994, a description of it was anonymously posted to the Cypherpunks mailing list. It was soon 
    posted on the sci.crypt newsgroup, where it was broken within days by Bob Jenkins. From there, it spread to many 
    sites on the Internet. The leaked code was confirmed to be genuine, as its output was found to match that of 
    proprietary software using licensed RC4. Because the algorithm is known, it is no longer a trade secret. The name 
    RC4 is trademarked, so RC4 is often referred to as ARCFOUR or ARC4 (meaning alleged RC4) to avoid trademark problems. 
    RSA Security has never officially released the algorithm; Rivest has, however, linked to the English Wikipedia 
    article on RC4 in his own course notes in 2008 and confirmed the history of RC4 and its code in a 2014 paper by him.""")
    st.markdown("---")

    with st.form('rc4 encoding'):
        plain_text = st.text_area(
            "**Please, input your text to be ciphered**",
            value="Meine kleine Swester hat ein Handchen!"
        )
        key = st.text_area(
            "**Please, input your key**",
            value="not-so-random-key"
        )
        n = st.number_input('Insert the number pf bits to be considered at a time', min_value=1, max_value=8,
                            value=1, step=1)

        st.form_submit_button("Encrypt")
        ciphertext = encryption(key, plain_text, n)
        st.write("Encryption result:")
        st.code(ciphertext)


    '''with st.form("TC4 decoding"):
        st.form_submit_button("Decryption")
        decrypted = decrypt(key, ciphertext)
        st.write(decrypted)'''


if __name__ == "__main__":
    main()