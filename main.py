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
    global RAID_5_1
    global RAID_5_2



    if(disks_index < 3):
        problematische_Raid = RAID_5_1
        problematische_index = disks_index
    else:
        problematische_Raid = RAID_5_2
        problematische_index = disks_index - 3


    lost_data = []
    list_of_data = []
    for i in range(len(problematische_Raid)):
        if i != problematische_index:
            file = open(problematische_Raid[i], 'r')
            list_of_data += [file.readlines()]
            file.close()
        else:
            list_of_data += ["*" * (len(disks_indexes) - 1)]



    for i in range(len(list_of_data[0])):
        small_list_of_data = []
        for j in range(len(list_of_data)):
            small_list_of_data.append(list_of_data[j][i])

        indexes = [x for x in range(len(small_list_of_data)) if small_list_of_data[x] != '*']

        lost_data.append(xor_two_str(small_list_of_data[indexes[0]][:-1:], small_list_of_data[indexes[1]][:-1:])[2::])


    for i in range(len(lost_data)):
        while (len(lost_data[i]) < 3):
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
    global disks_indexes
    if (len(disks_indexes) == 1):
        print('Disks are empty.')
        return
    else:
        print('Array size is {}'.format(disks_indexes[-1] + 1))
    check_disks()
    while (True):
        input_data = input("Enter the index of the line you want to read or enter \"-1\" to leave: ")
        if int(input_data) == -1:
            return
        elif int(input_data) > disks_indexes[-1]:
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
            if(list_of_data[i][int(input_data)] == ""):
                res += "0000"
            else:
                list_of_data[i][int(input_data)] = list_of_data[i][int(input_data)][:-1]
                if len(res) == 0 or len(res) == 7:
                    while(len(list_of_data[i][int(input_data)]) < 4):
                        list_of_data[i][int(input_data)] = "0" + list_of_data[i][int(input_data)]
                    res += list_of_data[i][int(input_data)]
                else:
                    while (len(list_of_data[i][int(input_data)]) < 3):
                        list_of_data[i][int(input_data)] = "0" + list_of_data[i][int(input_data)]
                    res += list_of_data[i][int(input_data)]

    print("Data on the address {}:".format(input_data))
    print(res)


def write() -> None:
    check_disks()
    if (disks_indexes[-1] == 63):
        print('Disks are full.')
        return


    while (True):
        input_data = str(input("Enter the string: "))
        if len(input_data) != 14:
            print("String length is not equal to 14 bytes.")
        else:
            break
    blocks = [input_data[:4], input_data[4:7], input_data[7:11], input_data[11:14]]
    for i in range(len(blocks)):
        while (len(blocks[i]) < 3):
            blocks[i] = '0' + blocks[i]

    excess_data1 = xor_two_str(blocks[0], blocks[1])[2::]
    excess_data2 = xor_two_str(blocks[2], blocks[3])[2::]


    disks_indexes.append(disks_indexes[-1] + 1)


    l1 = ['', '', '']
    l2 = ['', '', '']

    l1[disks_indexes[-1] % 3] = excess_data1
    l2[disks_indexes[-1] % 3] = excess_data2
    indexes = [x for x in range(len(l1)) if x != disks_indexes[-1] % 3]

    l1[indexes[0]] = blocks[0]
    l2[indexes[0]] = blocks[2]

    l1[indexes[1]] = blocks[1]
    l2[indexes[1]] = blocks[3]

    for i in range(len(RAID_5_1)):
        file_1 = open(RAID_5_1[i], 'a')
        file_2 = open(RAID_5_2[i], 'a')

        file_1.write(l1[i] + '\n')
        file_2.write(l2[i] + '\n')

        file_1.close()
        file_2.close()
    print('The data were recorded with an index of {}.'.format(disks_indexes[-1]))


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


