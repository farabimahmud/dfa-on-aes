import numpy as np
from scipy.stats import mode
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


def get_master_key_from_recovered(rk, starting_round=9):
    print("{} & {} \\\\ \\hline".format(starting_round+1, rk))
    for r in range(starting_round,-1,-1):
        rk = bytes_to_str(prev_roundkey(str_to_bytes(rk),rc[r]))
        print("{} & {} \\\\ \\hline".format(r, rk))
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
    input_filename = "set2.txt"
    correct_ciphers= []
    faulty_ciphers = []
    correct_ciphers, faulty_ciphers = process_input(input_filename)
    data = [[] for i in range(4)]
    c = correct_ciphers[0]

    for i in range(20):
        d = faulty_ciphers[i]
        x = dfa_byte_fault(c,d)
        fault_location = find_fault_byte_index(c,d)
        if (x is []):
            continue
        else:
            if len(data[fault_location]) == 0:
                data[fault_location] = np.array(x)
            else:
                data[fault_location] = np.append(data[fault_location],x,axis=0)

    guess = np.array([])   
    for i in range(4):
        if len(data[i]) != 0:
            if len(guess)==0:
                guess = np.array(find_most_common_elem(data[i]))
                guess = guess.reshape(1,16)
            else:  
                guess = np.append(guess,np.array(find_most_common_elem(data[i])).reshape(1,16),axis=0)
    r10_key = guess.max(axis=0).tolist()
    master_key = get_master_key_from_recovered(bytes_to_str(r10_key))
    print("Master Key {}".format(master_key))
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

def dfa_byte_fault_b0(c,d):
    recovered = []
    for f in range(256):
        valid = [0,0,0,0]
        for k0 in range(256):
            if 2 * f == inv_subbyte(c[0] ^ k0) ^ inv_subbyte(d[0]^k0):
                valid[0] =1
            else:
                continue
            for k13 in range(256):
                if f == inv_subbyte(c[13] ^ k13) ^ inv_subbyte(d[13]^k13):
                    valid[1] =1
                else:
                    continue
                for k10 in range(256):
                    if f == inv_subbyte(c[10] ^ k10) ^ inv_subbyte(d[10]^k10):
                        valid[2] =1
                    else:
                        continue   
                    for k7 in range(256):
                        if 3*f == inv_subbyte(c[7] ^ k7) ^ inv_subbyte(d[7]^k7):
                            valid[3] =1
                            if (sum(valid)==4):
                                recovered.append([
                                    k0, -1,  -1, -1,
                                    -1, -1,  -1, k7,
                                    -1, -1, k10, -1,
                                    -1, k13, -1, -1])

    return recovered
                         


def dfa_byte_fault_b1(c,d):
    recovered = []
    for f in range(256):
        valid = [0,0,0,0]
        for k4 in range(256):
            if 3 * f == inv_subbyte(c[4] ^ k4) ^ inv_subbyte(d[4]^k4):
                valid[0]=1
            else:
                continue
            for k1 in range(256):
                if 2* f == inv_subbyte(c[1] ^ k1) ^ inv_subbyte(d[1]^k1):
                    valid[1]=1
                else:
                    continue
                for k14 in range(256):
                    if f == inv_subbyte(c[14] ^ k14) ^ inv_subbyte(d[14]^k14):
                        valid[2]=1
                    else:
                        continue   
                    for k11 in range(256):
                        if f == inv_subbyte(c[11] ^ k11) ^ inv_subbyte(d[11]^k11):
                            valid[3]=1
                            if (sum(valid)==4):
                                recovered.append([
                                    -1, k1, -1, -1,
                                    k4, -1, -1, -1,
                                    -1, -1, -1, k11,
                                    -1, -1, k14,-1])

    return recovered


def dfa_byte_fault_b2(c,d):
    recovered = []
    for f in range(256):
        valid = [0,0,0,0]
        for k8 in range(256):
            if  f == inv_subbyte(c[8] ^ k8) ^ inv_subbyte(d[8]^k8):
                valid[0]=1
            else:
                continue
            for k5 in range(256):
                if 3* f == inv_subbyte(c[5] ^ k5) ^ inv_subbyte(d[5]^k5):
                    valid[1]=1
                else:
                    continue
                for k2 in range(256):
                    if 2*f == inv_subbyte(c[2] ^ k2) ^ inv_subbyte(d[2]^k2):
                        valid[2]=1
                    else:
                        continue   
                    for k15 in range(256):
                        if f == inv_subbyte(c[15] ^ k15) ^ inv_subbyte(d[15]^k15):
                            valid[3]=1
                            if (sum(valid)==4):
                                recovered.append([
                                    -1, -1, k2, -1,
                                    -1, k5, -1, -1,
                                    k8, -1, -1, -1,
                                    -1, -1, -1, k15])                            
    return recovered


def dfa_byte_fault_b3(c,d):
    recovered = []
    for f in range(256):
        valid = [0,0,0,0]

        for k3 in range(256):
            if  2 * f == inv_subbyte(c[3] ^ k3) ^ inv_subbyte(d[3]^k3):
                valid[0] = 1
            else:
                continue
            for k6 in range(256):
                if 3 * f == inv_subbyte(c[6] ^ k6) ^ inv_subbyte(d[6]^k6):
                    valid[1] = 1
                else:
                    continue
                for k9 in range(256):
                    if f == inv_subbyte(c[9] ^ k9) ^ inv_subbyte(d[9]^k9):
                        valid[2] = 1
                    else:
                        continue   
                    for k12 in range(256):
                        if f == inv_subbyte(c[12] ^ k12) ^ inv_subbyte(d[12]^k12):
                            valid[3] = 1
                            # print("Valid K3 {} K6 {} K9 {} K12".format(k3,k6, k9, k12), valid)
                            if sum(valid)==4:
                                recovered.append([
                                    -1, -1, -1, k3,
                                    -1, -1, k6, -1,
                                    -1, k9, -1, -1,
                                    k12,-1,-1, -1])

    return recovered



def dfa_byte_fault(c,d):    
    fault_byte = find_fault_byte_index(c,d)
    # print(fault_byte)
    recovered = []
    if  fault_byte == 0:
        recovered = dfa_byte_fault_b0(c,d)
    elif fault_byte == 1:
        recovered = dfa_byte_fault_b1(c,d)
    elif fault_byte == 2:
        recovered = dfa_byte_fault_b2(c,d)    
    elif fault_byte == 3:
        recovered = dfa_byte_fault_b3(c,d)
    return recovered

def find_most_common_elem(mat):
    v, c = mode(mat, axis=0)
    return v.ravel().tolist()



if __name__ == "__main__":
    task2()