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



def next_rounkdey(arr, round_constant):
    next_arr = []
    w0 = [arr[0],arr[1],arr[2],arr[3]]
    w1 = [arr[4],arr[5],arr[6],arr[7]]
    w2 = [arr[8],arr[9],arr[10],arr[11]]
    w3 = [arr[12],arr[13],arr[14],arr[15]]
    gw3 = gfunction(w3, round_constant)
    w4 = [x^y for x,y in zip(w0,gw3)]
    w5 = [x^y for x,y in zip(w4,w1)]
    w6 = [x^y for x,y in zip(w5,w2)]
    w7 = [x^y for x,y in zip(w6,w3)]
    next_arr.extend(w4)
    next_arr.extend(w5)
    next_arr.extend(w6)
    next_arr.extend(w7)

    return next_arr

def prev_roundkey(arr, round_constant):
    prev_arr = []
    w4 = [arr[0],arr[1],arr[2],arr[3]]
    w5 = [arr[4],arr[5],arr[6],arr[7]]
    w6 = [arr[8],arr[9],arr[10],arr[11]]
    w7 = [arr[12],arr[13],arr[14],arr[15]]

    w3 = [x^y for x,y in zip(w6,w7)]
    gw3 = gfunction(w3, round_constant)
    w2 = [x^y for x,y in zip(w5,w6)]
    w1 = [x^y for x,y in zip(w4,w5)]
    w0 = [x^y for x,y in zip(w4,gw3)]
    prev_arr.extend(w0)
    prev_arr.extend(w1)
    prev_arr.extend(w2)
    prev_arr.extend(w3)

    return prev_arr


def get_master_key_from_recovered(rk):
    for r in range(9,-1,-1):
        rk = bytes_to_str(prev_roundkey(str_to_bytes(rk),rc[r]))
        # print(r, rk)
    return rk 


def task1():
    input_filename = "set1.txt"
    correct_ciphers = []
    faulty_ciphers = []
    correct_ciphers, faulty_ciphers = process_input(input_filename)

    recovered = dfa_bit_fault(correct_ciphers,faulty_ciphers)
    master_key = get_master_key_from_recovered(bytes_to_str(recovered))
    print("Master Key {}".format(master_key))
    return master_key

def task2():
    master_key = ''
    return master_key

def find_fault_byte_index(c,d):
    locations = find_non_zero_locations(c,d)
    if 0 in locations:
        return 0
    elif 1 in locations:
        return 1
    elif 2 in locations:
        return 2
    elif 3 in locations:
        return 3
    else:
        print("Error!")
        exit(1)

if __name__ == "__main__":
    task1()
    # print(bytes_to_str(recovered))
    # rk = '5468617473206D79204B756E67204675'
    # print(bytes_to_str(next_rounkdey(str_to_bytes(rk0),rc[0])))
    # for r in range(0,10,1):
    #     rk = bytes_to_str(next_rounkdey(str_to_bytes(rk),rc[r]))
    #     print(r, rk)
    # test r10 28fddef86da4244accc0a4fe3b316f26
    # test r0 

    # print(bytes_to_str(prev_roundkey(str_to_bytes(rk1),rc[0])))
    input_filename = "set2.txt"
    correct_ciphers= []
    faulty_ciphers = []
    correct_ciphers, faulty_ciphers = process_input(input_filename)

    for d in faulty_ciphers:
        print(find_fault_byte_index(correct_ciphers[0],d))