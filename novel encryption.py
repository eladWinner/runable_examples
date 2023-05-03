import decimal
import math
import os.path
import random

size_edge = 16  # sqrt of byte max value
se2 = size_edge ** 2

decimal.getcontext().prec = se2


class encryption_class():
    def __init__(self, key):
        self.key = key
        spots = []
        temp = 0
        for digit in (decimal.Decimal(key) / decimal.Decimal(math.e)).as_tuple()[1]:
            temp += digit + 2
            spots.append(temp)
        self.spots = spots

    def decode(self, file_path: str, save_at=''):
        inv_order = [None] * se2
        order = [None] * se2
        end_file = file_path.rindex("\\") + 1
        file_start = file_path[:end_file]
        file_name = file_path[end_file:]
        if file_name[:10] == "encrypted_":
            file_name = file_name[10:]
        file_name = "decrypted_" + file_name
        index = 0
        s_index = 0
        shiter_x = 0
        shiter_y = 0
        with open(file_path, 'rb') as file_read:
            while True:
                byte_read = file_read.read(1)
                if not byte_read:
                    exit("file too small to decrypt")
                if s_index < se2 and index == self.spots[s_index]:
                    order[s_index] = byte_read
                    unsigned_int = int.from_bytes(byte_read, "little", signed=False)
                    inv_order[unsigned_int] = s_index
                    s_index += 1
                    if s_index == se2:
                        break
                index += 1
        s_index = 0
        index = 0
        if not len(save_at):
            save_at = file_start + file_name
        with open(file_path, 'rb') as file_read:
            if not os.path.isfile(save_at):
                open(save_at, 'x')
            with open(save_at, 'wb') as file_write:
                prev_byte_data = None
                while True:
                    byte_read = file_read.read(1)
                    if not byte_read:
                        break
                    if s_index < se2 and index == self.spots[s_index]:
                        s_index += 1
                        index += 1
                        shiter_x += 1
                        if shiter_x == size_edge:
                            shiter_y += 1
                            shiter_x = 0
                        continue
                    index += 1
                    if not prev_byte_data:
                        prev_byte_data = byte_read
                        continue
                    unsigned_prev = int.from_bytes(prev_byte_data, "little", signed=False)
                    unsigned_int = int.from_bytes(byte_read, "little", signed=False)
                    unsigned_int = int.from_bytes(order[unsigned_int], "little", signed=False)
                    unsigned_int -= shiter_x + shiter_y * size_edge + int.from_bytes(order[unsigned_prev], "little",
                                                                                     signed=False)
                    unsigned_int %= se2
                    to_write = unsigned_int.to_bytes(1, "little")
                    file_write.write(to_write)
                    prev_byte_data = None

    def incode(self, file_path: str, save_at=''):
        order = [i for i in range(se2)]
        random.shuffle(order)
        random.shuffle(order)  # XD
        inv_order = [None] * se2
        for i, val in enumerate(order):
            inv_order[val] = i
        end_file = file_path.rindex("\\") + 1
        file_start = file_path[:end_file]
        file_name = file_path[end_file:]
        index = 0
        s_index = 0
        shiter_x = 0
        shiter_y = 0
        if not len(save_at):
            save_at = file_start + "encrypted_" + file_name
        with open(file_path, 'rb') as file_read:
            if not os.path.isfile(save_at):
                open(save_at, 'x')
            with open(save_at, 'wb') as file_write:
                while True:
                    byte_read = file_read.read(1)
                    if not byte_read:
                        if s_index < se2:
                            exit("file too small to encrypt " + str(s_index))
                        break
                    if s_index < se2 and index == self.spots[s_index]:
                        file_write.write(order[s_index].to_bytes(1, "little"))
                        s_index += 1
                        index += 1
                        shiter_x += 1
                        if shiter_x == size_edge:
                            shiter_y += 1
                            shiter_x = 0
                    rand = random.randint(0, se2 - 1)
                    val = inv_order[rand]
                    to_write = val.to_bytes(1, "little")
                    file_write.write(to_write)
                    index += 1
                    if s_index < se2 and index == self.spots[s_index]:
                        file_write.write(order[s_index].to_bytes(1, "little"))
                        s_index += 1
                        index += 1
                        shiter_x += 1
                        if shiter_x == size_edge:
                            shiter_y += 1
                            shiter_x = 0
                    unsigned_int = int.from_bytes(byte_read, "little", signed=False)
                    unsigned_int += shiter_x + shiter_y * size_edge + rand
                    unsigned_int %= se2
                    val = inv_order[unsigned_int]
                    to_write = val.to_bytes(1, "little")
                    file_write.write(to_write)
                    index += 1

def show_histo(file):  # i asked chatgpt to test my encrypted file entropy
    import collections
    import matplotlib.pyplot as plt
    import numpy as np

    # Open the file and read its contents
    with open(file, 'rb') as f:
        data = f.read()

    # Convert the data into a list of bytes
    bytes_list = bytes(data)

    # Count the occurrence of each byte
    counter = collections.Counter(bytes_list)

    # Plot the histogram
    plt.bar(counter.keys(), counter.values())
    plt.title("histogram of bytes in encrypted file")
    plt.show()
    # Compute the difference between adjacent bytes
    int_list = [int(byte) for byte in bytes_list]
    byte_diff = np.diff(int_list)
    byte_diff = byte_diff % 256

    # Count the occurrence of each difference value

    diff_counter = collections.Counter(byte_diff)

    # Plot the histogram
    plt.bar(diff_counter.keys(), diff_counter.values())
    plt.title("histogram of difference between adjacent bytes")
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("running")
    encryptor = encryption_class(4 - 2 ** -51)  # 2**-51 is minimum key resolution
    path_to_text = 'fill here' # path to text.txt file
    if path_to_text == 'fill here':
        raise not "given path"
    encryptor.incode(path_to_text + "text.txt")
    encryptor.decode(path_to_text + "encrypted_text.txt")
    bad_encryptor = encryption_class(4)
    bad_encryptor.decode(path_to_text + "encrypted_text.txt", save_at=path_to_text + "bad_encrypted_text.txt")

    show_histo(path_to_text + "encrypted_text.txt")

