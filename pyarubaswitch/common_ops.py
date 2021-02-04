def shorten_numberlist(numbers, verbose=False):
    '''Takes a list of numbers(in string format), returns a shortened list of numbers ie
        ['2','4','5','6','9','15','16','17'] returns: ['2','4-6','9','15-17'].
        verbose=True prints information on whats happening each way through the loop for debugging.'''
    # empty lists will be appended to in the for loop
    num_list = []
    consec_number_list = []
    prev_num = None

    for num in numbers:
        # its a list of numbers in string format, convert to integer.
        num = int(num)

        # if there was no prev number
        if prev_num == None:
            if verbose:
                print(f"{num} is first in range")

            prev_num = num
            num_list.append(num)
        # if number is +1 from prev
        elif num == prev_num + 1:
            if verbose:
                print(f"{num} is +1 from {prev_num}")

            num_list.append(num)
            prev_num = num
        # number is not +1 from prev
        elif num != prev_num + 1:
            if verbose:
                print(f"{num} is NOT +1 from {prev_num}")
                print(f"Writing last finished range: {num_list} ")

            prev_num = num
            # if there is more than one number in list append firts and last int with - in between.
            if len(num_list) > 1:
                consec_number_list.append(f"{num_list[0]}-{num_list[-1]}")
            elif len(num_list) > 0:
                # only one number in list, append only that number in string format.
                consec_number_list.append(f"{num_list[0]}")
            # new list of numbers is empty and starts with this new number
            num_list = []
            if verbose:
                print(f"{num} is therefore first in range, adding to new list")

            num_list.append(num)

    # the last numbers goes outside the loop. Cannot think of a prettier way to do this right now
    if verbose:
        print(num_list)

    # if there is more than one number in list append firts and last int with - in between.
    if len(num_list) > 1:
        consec_number_list.append(f"{num_list[0]}-{num_list[-1]}")
    elif len(num_list) > 0:
        # only one number in list, append only that number in string format.
        consec_number_list.append(f"{num_list[0]}")

    if verbose:
        print(f"FINISHED conseclist: {consec_number_list}")

    return consec_number_list
