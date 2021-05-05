


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
      
if __name__ == "__main__":
    input_filename = "set1.txt"
    correct_ciphers = []
    faulty_ciphers = []
    correct_ciphers, faulty_ciphers = process_input(input_filename)
    print(len(faulty_ciphers))
    