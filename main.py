
def shift_row_index(i):
    if i %4 == 0: 
        return i 
    elif i == 1:
        return 5
    elif i == 5:
        return 9
    elif i == 9:
        return 13
    elif i == 13:
        return 1
    
    elif i == 2:
        return 10
    elif i == 6:
        return 14
    elif i == 10:
        return 2
    elif i == 14:
        return 6

    elif i == 3:
        return 15
    elif i == 7:
        return 3
    elif i == 11:
        return 7
    elif i == 15:
        return 11 
    else:
        print("Error: i should be in range [0,15]")
        exit(1)

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

def dfa_bit_fault():
    locations = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80]
    for x in range(255):
        for e in locations:
            pass
    return 0

if __name__ == "__main__":
    input_filename = "set1.txt"
    correct_ciphers = []
    faulty_ciphers = []
    correct_ciphers, faulty_ciphers = process_input(input_filename)
    print(faulty_ciphers[2])