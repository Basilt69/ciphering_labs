import streamlit as st
import pandas as pd

from collections import Counter


class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        # probability of symbol
        self.prob = prob

        # symbol
        self.symbol = symbol

        # left
        self.left = left

        # right
        self.right = right

        # tree direction (0/1)
        self.code = ''


"""a helper function to print the codes of symbols by traveling Huffman tree"""
codes = dict()


def calculate_codes(node, val=''):
    # huffman code for current node
    new_val = val + str(node.code)
    if node.left:
        calculate_codes(node.left, new_val)
    if node.right:
        calculate_codes(node.right, new_val)
    if not node.left and not node.right:
        codes[node.symbol] = new_val

    return codes


"""A helper function to calculate the probabilities of symbols in given data"""


def calculate_probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) is None:
            symbols[element] = 1
        else:
            symbols[element] += 1
    return symbols


"""A helper function to obtain the encoded output"""


def output_encoded(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])

    string = ''.join([str(item) for item in encoding_output])
    return string


"""A helper function to calculate the space difference between compressed and non-compressed data"""


def total_gain(data, coding):
    before_compression = len(data) * 8 # total bit space to store the data before compression
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol])
    return before_compression, after_compression


def huffman_encoding(data):
    symbol_with_probs = calculate_probability(data)
    symbols = symbol_with_probs.keys()
    #probabilities = symbol_with_probs.values()
    st.write("Symbols: ", symbols)
    #st.write("Probabilities: ", probabilities)

    nodes = []

    # converting symbols and probabilities into huffman tree nodes
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))

    while len(nodes) > 1:
        #sort all the nodes in scending order based on their probability
        nodes = sorted(nodes, key=lambda x: x.prob)

        # pick two smallest nodes
        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        # combine the 2 smallest nodes to create new node
        new_node = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)

    encoding_res = calculate_codes(nodes[0])

    freq = pd.DataFrame.from_dict(dict(Counter(data)), orient="index", columns=["Frequency"])
    df = pd.DataFrame.from_dict(encoding_res, orient="index", columns=["Code"])
    merged_df = freq.merge(df, left_index=True, right_index=True).sort_values(by="Frequency")
    st.write("Symbols with frequency and code:", merged_df)

    before_comp, after_comp = total_gain(data, encoding_res)
    encoded_output = output_encoded(data, encoding_res)

    return encoded_output, nodes[0], before_comp, after_comp


def huffman_decoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol is None and huffman_tree.right.symbol is None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head

    string = ''.join([str(item) for item in decoded_output])
    return string



def main():
    st.markdown("## Laboratory work №4")
    st.markdown("### **Title**: Huffman compression")
    st.markdown("---")

    st.markdown("""**Huffman code** is a particular type of optimal prefix code that is commonly used for lossless 
                      data compression. The process of finding or using such a code proceeds by means of Huffman coding,
                      an algorithm developed by David A. Huffman while he was a Sc.D. student at MIT, and published in 
                      the 1952 paper 'A Method for the Construction of Minimum-Redundancy Codes'""")
    st.markdown("---")

    with st.form('huffman encoding'):
        message = st.text_area(
            "**Please, input your text to be compressed**",
            value="Meine kleine Swester hat ein Handchen!"
        )
        st.form_submit_button("Compress")
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