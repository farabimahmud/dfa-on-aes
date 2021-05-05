


def process_input(filename):
    correct_ciphers = []
    faulty_ciphers = []
    with open(filename, "r") as f:
        for lines in f:
            data = lines.split(":")
            cipher_type = data[0].strip()
            cipher_text = data[1].strip()
            print(cipher_type, cipher_text)
            if cipher_type == "Faulty":
                faulty_ciphers.append(cipher_text)
            elif cipher_type == "Correct":
                correct_ciphers.append(cipher_text)
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
if __name__ == "__main__":
    input_filename = "set1.txt"
    correct_ciphers = []
    faulty_ciphers = []
    correct_ciphers, faulty_ciphers = process_input(input_filename)
    print(len(faulty_ciphers))
    a = str_to_bytes(correct_ciphers[0])
    print_state(a)