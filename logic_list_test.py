ports = [ 1, 2, 3, 2, 2, 1, 1, 1]

ports_set = set(ports)

print(f'listan: {ports}')
print(f'Numbers list, disregarding duplicates lenght: {len(ports_set)}')

print(f'Unique: {ports_set}')

for i in ports_set:
    # for each unnique value

    #find number of occurenses in list  
    occur = ports.count(i)
    print(f'number: {i}')
    print(occur)