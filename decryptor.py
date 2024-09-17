import sys


# decodes fib
def fib_decode(code):
    fib = [1, 2]
    decoded_value = 0
    # checks if fib number included in fib code, if so tallies it
    for i in range(len(code) - 1):
        fib.append(fib[-1] + fib[-2])
        if code[i] == "1":
            decoded_value += fib[i]
    return decoded_value


# changes binary to ascii
def ascii_decode(code):
    return chr(int(code, 2))


# traverses the binary, stops when it hits 11 (signal to stop for fib code)
# returns the fib value found as well as where the index binary is not traversed
def find_fib(code, current):
    start = current
    prev = 0
    # makes sure we aren't already near the end of binary
    if current < len(code) - 1:
        done = False
    else:
        done = True
    # traverses binary
    while not done:
        if code[current] == "1" and prev == "1":
            done = True
        prev = code[current]
        current += 1
        if current > len(code) - 1:
            done = True
    fib = fib_decode(code[start:current])
    return fib, current


# decodes the binary code
def decoding(code, password):
    code = decrypt(code, password)
    # decoding first input (bwt length)
    bwt_len, current = find_fib(code, 0)
    # decoding second input (number of unique characters)
    freq_len, current = find_fib(code, current)
    # decoding huffman values and ascii representation of each unique character
    characters = []
    huff = []
    for _ in range(freq_len):
        # decodes character
        current_character = ascii_decode(code[current:current + 7])
        characters.append(current_character)
        current += 7
        huff_len, current = find_fib(code, current)
        # stores huff code
        huff_val = ""
        for _ in range(huff_len):
            huff_val += code[current]
            current += 1
        huff.append(huff_val)
    # decoding run length tuples
    in_order_characters = []
    run_length = []
    while current < len(code) - 3:
        huff_val = ""
        while huff_val not in huff:
            huff_val += code[current]
            current += 1
        current_character = characters[huff.index(huff_val)]
        in_order_characters.append(current_character)
        current_run_length, current = find_fib(code, current)
        run_length.append(current_run_length)
    output = ""
    # translating run length tuples to string output
    for i in range(len(run_length)):
        for j in range(run_length[i]):
            output += in_order_characters[i]
    return output


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


def decrypt(code, password):
    output = code
    for i in range(len(password) - 1, -1, -1):
        output = le_flip(output, ord(password[i]))
        output = le_flip(output, len(str(ord(password[i]))))
        for j in range(len(str(ord(password[i]))) - 1, -1, -1):
            output = le_flip(output, int(str(ord(password[i]))[j]))
    output = le_full_flip(output)
    return output


if __name__ == '__main__':
    decoded_message = str(sys.argv[1])
    password_encoder = str(sys.argv[2])
    output_file = str(sys.argv[3])
    with open(decoded_message) as f:
        line = f.readline()
        txtinput = str(line)
    with open(password_encoder) as f:
        line = f.readline()
        passinput = str(line)
    with open(output_file, "w") as f:
        f.write(decoding(txtinput, passinput))
