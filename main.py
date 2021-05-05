import numpy as np
from aes import *

def process_input(filename):
    correct_ciphers = []
    faulty_ciphers = []
    with open(filename, "r") as f:
        for lines in f:
            data = lines.split(":")
            cipher_type = data[0].strip()
            cipher_text = data[1].strip()
            # print(cipher_type, cipher_text)
            if cipher_type == "Faulty":
                faulty_ciphers.append(str_to_bytes(cipher_text))
            elif cipher_type == "Correct":
                correct_ciphers.append(str_to_bytes(cipher_text))
    return correct_ciphers, faulty_ciphers

def bytes_to_str(arr):
    s = ''
    for i in arr:
        s = s+ "{:02x}".format(i)
    return s  

def str_to_bytes(line):
    arr = [ '' for i in range(16)]

    k = 0
    for i in range(len(line)):
        arr[k]= arr[k]+line[i]
        i = i+1
        if i%2 == 0:
            k = k+1 
    for i in range(16):
        arr[i] = int(arr[i],base=16)
    return arr 

def print_state(a):
    for i in range(4):
        for j in range(4):
            print("{:02x}".format(a[i*4+j]), end=" ")
    print()

def dfa_bit_fault(c, ds):
    
    locations = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
    recovered = []
    for j in range(16):
        count = [0]*255
        for x in range(255):
            for e in locations:
                for d in ds:
                    lhs = c[0][shift_row_index(j)] ^ d[shift_row_index(j)]
                    rhs = subbyte(x) ^ subbyte(x ^ e)
                    if (lhs == rhs):
                        count[x] = count[x]+1
        recovered.append(np.argmax(count))
    return recovered

def find_non_zero_locations(c, d):
    res = []
    for i in range(16):
        if (c[i] ^ d[i] != 0):
            res.append(i)
    return res 


if __name__ == "__main__":
    input_filename = "set1.txt"
    correct_ciphers = []
    faulty_ciphers = []
    correct_ciphers, faulty_ciphers = process_input(input_filename)

    recovered = dfa_bit_fault(correct_ciphers,faulty_ciphers)
    print(bytes_to_str(recovered))
    