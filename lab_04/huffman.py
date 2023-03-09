import streamlit as st


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


def Calculate_Codes(node, val=''):
    # huffman code for current node
    newVal = val + str(node.code)

    if (node.left):
        Calculate_Codes(node.left, newVal)
    if (node.right):
        Calculate_Codes(node.right, newVal)

    if (not node.left and not node.right):
        codes[node.symbol] = newVal

    return codes


"""A helper function to calculate the probabilities of symbols in given data"""
def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) == None:
            symbols[element] = 1
        else:
            symbols[element] += 1
    return symbols


"""A helper function to obtain the encoded output"""
def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
        st.write(coding[c], end = '')
        encoding_output.append(coding[c])

    string = ''.join([str(item) for item in encoding_output])
    return string


"""A helper function to calculate the space difference between compressed and non-compressed data"""
def Total_Gain(data, coding):
    before_compression = len(data) * 8 # total bit space to store the data before compression
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol])
    st.markdown("Space usage before compression (in bits)", before_compression)
    st.markdown("Space usage after compression (in bits)", after_compression)


def Huffman_Encoding(data):
    symbol_with_probs = Calculate_Probability((data))
    symbols = symbol_with_probs.keys()
    probabilities = symbol_with_probs.values()
    st.markdown("Symbols: ", symbols)
    st.markdown("Probabilities: ", probabilities)

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
        newNode = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    huffman_encoding = Calculate_Codes(nodes[0])
    st.markdown(huffman_encoding)
    Total_Gain(data, huffman_encoding)
    encoded_output = Output_Encoded(data, huffman_encoding)
    st.markdown("Encoded output: ", encoded_output)
    return encoded_output, nodes[0]


def Huffman_Decoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
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

    description_huf = "Huffman code is a particular type of optimal prefix code that is commonly used for lossless " \
                      "data compression. The process of finding or using such a code proceeds by means of Huffman coding," \
                      "an algorithm developed by David A. Huffman while he was a Sc.D. student at MIT, and published in " \
                      "the 1952 paper 'A Method for the Construction of Minimum-Redundancy Codes'"

    show_schema = st.checkbox("Show description:")
    if show_schema:
        st.code(description_huf)

    st.markdown("**Please, input your text**")
    message = st.text_input("(All your text and punctuation will be compressed")

    encoding, tree = Huffman_Encoding(message)
    st.markdown("Encoded output: ", encoding)

    st.markdown("Decoded output", Huffman_Decoding(encoding, tree))


if __name__ == "__main__":
    main()