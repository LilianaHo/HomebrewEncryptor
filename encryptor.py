import sys


# class for the node (for huffman construction)
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        self.code = ""

    def __repr__(self):
        return str(self.char) + " with frequency of " + str(self.freq)


# lists the huffman codes using the aux and then makes the value more readable (done once huffman is constructed)
def node_values(node):
    result = node_values_aux(node, "")
    clean_result = []
    for i in range(0, len(result), 2):
        clean_result.append([result[i], result[i + 1]])
    return clean_result


# traverses through and lists the huffman codes
def node_values_aux(node, aux):
    # aux value stores where you have traversed so far
    current_code = aux + str(node.code)
    result = []
    # if you can traverse further, do so
    if node.left or node.right:
        if node.left:
            result += node_values_aux(node.left, current_code)
        if node.right:
            result += (node_values_aux(node.right, current_code))
    # otherwise return the char and the code
    else:
        return node.char, current_code
    # returns list of huffman codes, to be cleaned up by node_values
    return result


# constructs the huffman trees and returns the huffman values
def huffman(chars, freq):
    # constructs list of nodes who have not yet been combined
    uncombined_nodes = []
    for i in range(len(chars)):
        uncombined_nodes.append(Node(chars[i], freq[i]))

    # while there are uncombined nodes
    while len(uncombined_nodes) >= 2:
        # find the 2 minimum node values
        min1, min2 = min_node_indexes(uncombined_nodes)
        left = uncombined_nodes[min1]
        right = uncombined_nodes[min2]
        # traversing left = 0 while right = 1
        left.code = 0
        right.code = 1
        # creates a combined node
        parent = Node(left.char + right.char, left.freq + right.freq, left, right)
        # removes nodes from uncombined nodes list
        uncombined_nodes.remove(left)
        uncombined_nodes.remove(right)
        # it is replaced with a new combined node
        uncombined_nodes.append(parent)
    return node_values(uncombined_nodes[0])


# calculates the two minimum value nodes
def min_node_indexes(uncombined_nodes):
    max_val = uncombined_nodes[0].freq
    min1_ind = 0
    min1_val = uncombined_nodes[0].freq
    for j in range(1, len(uncombined_nodes)):
        if uncombined_nodes[j].freq < min1_val:
            min1_ind = j
            min1_val = uncombined_nodes[j].freq
        if uncombined_nodes[j].freq >= max_val:
            max_val = uncombined_nodes[j].freq
    min2_ind = 0
    min2_val = max_val
    for k in range(len(uncombined_nodes)):
        if uncombined_nodes[k].freq <= min2_val and k != min1_ind:
            min2_ind = k
            min2_val = uncombined_nodes[k].freq
    return min1_ind, min2_ind


# generates the frequencies for each character
def freq_gen(string):
    chars = []
    freq = []
    # traverses string and tallies the frequencies
    for i in range(len(string)):
        if string[i] not in chars:
            chars.append(string[i])
            freq.append(1)
        else:
            for j in range(len(chars)):
                if string[i] == chars[j]:
                    freq[j] += 1
    return chars, freq


# generates all values of tbe Fibonacci sequence until final value is higher than num
def fib_gen(num):
    fib = [1, 2]
    while fib[-1] < num + 1:
        fib.append(fib[-1] + fib[-2])
    return fib


# Fibonacci codes a number
def fib_code(num):
    fib = fib_gen(num)
    code = [0] * len(fib)
    remaining = num
    # uses greedy algorithm and grabs the biggest possible number moving in descending order
    for i in range(len(fib) - 1, -1, -1):
        if remaining - fib[i] >= 0:
            code[i] = 1
            remaining -= fib[i]
    code[-1] = 1
    return code


# codes values
def encoding(bwt, password):
    # calculates bwt length
    # join() translates from list to string format
    bwt_len = "".join([str(i) for i in fib_code(len(bwt))])
    freq = freq_gen(bwt)
    # calculates freq length
    freq_len = "".join([str(i) for i in fib_code(len(freq[0]))])
    huff = huffman(freq[0], freq[1])
    # calculates distinct characters
    dist_char_output = ""
    for i in range(len(huff)):
        # stores character as a binary
        char = bin(ord(huff[i][0]))
        # removes the b
        if char[-7] == "b":
            binary = "0" + char[-6:]
        else:
            binary = char[-7] + char[-6:]
        # stores length of huff code
        huff_len = "".join([str(i) for i in fib_code(len(huff[i][1]))])
        dist_char_output += binary + huff_len + huff[i][1]
    # stores the string in running length format
    run_encoded_output = ""
    current_int = 1
    current_run = 1
    char_run_list = []
    char_run_freq = []
    while current_int < len(bwt):
        if bwt[current_int] == bwt[current_int - 1]:
            current_run += 1
            current_int += 1
        else:
            char_run_list.append(bwt[current_int - 1])
            char_run_freq.append(current_run)
            current_run = 1
            current_int += 1
    char_run_list.append(bwt[current_int - 1])
    char_run_freq.append(current_run)
    # translate previously calculated value in binary
    for j in range(len(char_run_list)):
        for k in range(len(huff)):
            if char_run_list[j] == huff[k][0]:
                run_encoded_output += huff[k][1] + "".join([str(i) for i in fib_code(char_run_freq[j])])
    # combines all 4 values into the output
    output = bwt_len + freq_len + dist_char_output + run_encoded_output
    # makes sure it fits exactly, fills rest of bit with 0 if need be
    while len(output) % 8 != 0:
        output += "0"
    encrypted_output = encrypt(output, password)
    return encrypted_output


def le_full_flip(binary):
    encrypt_binary = ""
    for i in range(len(binary)):
        if binary[i] == "1":
            encrypt_binary += "0"
        else:
            encrypt_binary += "1"
    return encrypt_binary


def le_flip(binary, pass_val):
    if pass_val == 0:
        return le_full_flip(binary)
    encrypt_binary = ""
    for i in range(len(binary)):
        if i % pass_val == 0:
            if binary[i] == "1":
                encrypt_binary += "0"
            else:
                encrypt_binary += "1"
        else:
            encrypt_binary += binary[i]
    return encrypt_binary


def encrypt(binary, password):
    output = le_full_flip(binary)
    for i in range(len(password)):
        for j in range(len(str(ord(password[i])))):
            output = le_flip(output, int(str(ord(password[i]))[j]))
        output = le_flip(output, ord(password[i]))
        output = le_flip(output, len(str(ord(password[i]))))
    return output


if __name__ == '__main__':
    # .txt !
    encoded_message = str(sys.argv[1])
    password_encoder = str(sys.argv[2])
    # .bin !
    output_file = str(sys.argv[3])
    with open(encoded_message) as f:
        line = f.readline()
        txtinput = str(line)
    with open(password_encoder) as f:
        line = f.readline()
        passinput = str(line)
    with open(output_file, "w") as f:
        f.write(encoding(txtinput, passinput))
