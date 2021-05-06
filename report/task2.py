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
