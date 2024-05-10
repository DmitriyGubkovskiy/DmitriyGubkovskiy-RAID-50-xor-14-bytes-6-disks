# Raid 50, xor, 14b, 6d

import os

disks = ['disk 0.txt', 'disk 1.txt', 'disk 2.txt', 'disk 3.txt', 'disk 4.txt', 'disk 5.txt']

RAID_5_1 = ['disk 0.txt', 'disk 1.txt', 'disk 2.txt']
RAID_5_2 = ['disk 3.txt', 'disk 4.txt', 'disk 5.txt']
disks_indexes = [-1]


def xor_two_str(a: str, b: str) -> str:
    return hex((int(a, base=16) ^ int(b, base=16)))


def reconstruction(disks_index: int) -> None:
    global disks_indexes
    lost_data = []
    list_of_data = []
    for i in range(len(disks)):
        if i != disks_index:
            file = open(disks[i], 'r')
            list_of_data += [file.readlines()]
            file.close()

    for i in range(len(list_of_data[0])):
        tmp_set_for_data = set()
        tmp_list_for_data = []
        for j in range(len(list_of_data)):
            tmp_set_for_data.add(list_of_data[j][i])
            tmp_list_for_data.append(list_of_data[j][i])
        if len(tmp_set_for_data) == 4:
            tmp_list_for_data.clear()
            tmp_list_for_data = [x[:-1:] for x in tmp_set_for_data]
            lost_data.append(
                xor_two_str(
                    xor_two_str(xor_two_str(tmp_list_for_data[0], tmp_list_for_data[1]), tmp_list_for_data[2]),
                    tmp_list_for_data[3])[2::]
            )
        elif len(tmp_set_for_data) == 5:
            tmp_list_for_data.insert(disks_index, '*')
            try:
                lost_data.append(tmp_list_for_data[disks_index + 3][:-1:])
            except:
                lost_data.append(tmp_list_for_data[disks_index - 3][:-1:])

    for i in range(len(lost_data)):
        while (len(lost_data[i]) < 4):
            lost_data[i] = '0' + lost_data[i]

    with open(disks[disks_index], 'w') as file:
        for x in lost_data:
            file.write(x + '\n')

    print("The disk {} was recovered.".format(disks_index))


def check_disks() -> None:
    for i in range(len(disks)):
        if not os.path.isfile(disks[i]):
            print("The disk {} was lost.".format(i))
            reconstruction(i)
            break


def read() -> None:
    check_disks()
    global disks_indexes
    check_disks()
    while (True):
        input_data = input("Enter the index of the line you want to read: ")
        if int(input_data) > disks_indexes[-1]:
            print("Wrong index.")
        else:
            break

    list_of_data = []

    for i in range(len(disks)):
        file = open(disks[i], 'r')
        list_of_data += [file.readlines()]
        file.close()

    res = ''
    for i in range(len(list_of_data)):
        if (int(input_data) % 3) != i and (int(input_data) % 3) + 3 != i:
            while (list_of_data[i][int(input_data)][0] == '0'):
                list_of_data[i][int(input_data)] = list_of_data[i][int(input_data)][1::]
            res += list_of_data[i][int(input_data)][:-1]

    print("Data on the address {}:".format(input_data))
    print(res)


def write() -> None:
    check_disks()
    if (len(disks_indexes) == 1):
        print('Disks are empty.')
    while (True):
        input_data = str(input("Enter the string: "))
        if len(input_data) > 14:
            print("The length of the string is limited to 14 bytes.")
        else:
            break
    blocks = [input_data[:4], input_data[4:7], input_data[7:11], input_data[11:14]]
    for i in range(len(blocks)):
        while (len(blocks[i]) < 4):
            blocks[i] = '0' + blocks[i]

    excess_data = xor_two_str(xor_two_str(blocks[0], blocks[1]), xor_two_str(blocks[2], blocks[3]))[2::]

    disks_indexes.append(disks_indexes[-1] + 1)
    while (len(excess_data) < 4):
        excess_data = '0' + excess_data

    l1 = ['', '', '']
    l2 = ['', '', '']

    l1[disks_indexes[-1] % 3] = excess_data
    l2[disks_indexes[-1] % 3] = excess_data
    for i in range(len(l1)):
        if l1[i] == '' and blocks[0] not in l1:
            l1[i] = blocks[0]
            l2[i] = blocks[2]
        elif l1[i] == '':
            l1[i] = blocks[1]
            l2[i] = blocks[3]

    for i in range(len(RAID_5_1)):
        file_1 = open(RAID_5_1[i], 'a')
        file_2 = open(RAID_5_2[i], 'a')

        file_1.write(l1[i] + '\n')
        file_2.write(l2[i] + '\n')

        file_1.close()
        file_2.close()
    print('The data was recorded.')


if __name__ == '__main__':
    file = open(RAID_5_1[0], 'r')
    for _ in range(len(file.readlines())):
        disks_indexes.append(disks_indexes[-1] + 1)
    file.close()
    while (True):
        print("Write data - 1.")
        print("Read data - 2.")
        print("Exit - 0.")
        x = input("Enter the command: ")
        if x == '1':
            write()
        elif x == '2':
            read()
        elif x == '0':
            break
        else:
            print("Wrong command.")
