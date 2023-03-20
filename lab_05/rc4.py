import streamlit as st
import codecs


MOD = 256

def KSA(key):
    '''Key Scheduling algorithm (from wikipedia)
        for i from 0 to 255
            S[i] := i
        endfor
        j := 0
        for i from 0 to 255
            j := (j + S[i] + key[i mod keylength]) mod 256
            swap values of S[i] and S[j]
        endfor
    '''
    key_length = len(key)
    # create the array "S"
    S = list(range(MOD)) # [0, 1, 2, ... , 255]
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i] # swap values

    return S


def PRGA(S):
    '''Psudo Random Generation Algorithm (from wikipedia):
       i := 0
       j := 0
       while GeneratingOutput:
           i := (i + 1) mod
           j := (j + S[i]) mod 256
           swap values of S[i] and S[j]
           K := S[(S[i] + S[j]) mod 256]
           output K
        endwhile
    '''

    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i] # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K




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
        message = st.text_area(
            "**Please, input your text to be ciphered**",
            value="Meine kleine Swester hat ein Handchen!"
        )
        st.form_submit_button("Encrypt")
        encoded, tree, size_before, size_after = huffman_encoding(message)
        st.write("Compression result:")
        st.code(encoded)
        st.write("Size of the text before the compression(bites): ", size_before)
        st.write("Size of the text after the compression(bites): ", size_after)

    with st.form("huffman decoding"):
        st.form_submit_button("Decompress")
        decoded = huffman_decoding(encoded, tree)
        st.write(decoded)


if __name__ == "__main__":
    main()