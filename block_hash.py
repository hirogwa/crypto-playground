import hashlib


def get_blocks(f):
    block_list = []
    while True:
        b = f.read(1024)
        if len(b) == 0:
            break
        else:
            block_list.append(b)
    return block_list


def convert_to_hashed_blocks(blocks):
    for i in range(-1, -len(blocks), -1):
        if i % 500 == 0:
            print('computing block at {}'.format(i))
        blocks[i-1] = blocks[i-1] + hashlib.sha256(blocks[i]).digest()
    return hashlib.sha256(blocks[0]).hexdigest(), blocks


def run(file_path):
    with open(file_path, "rb") as f:
        blocks = get_blocks(f)

    print('block count:{}'.format(len(blocks)))
    result = convert_to_hashed_blocks(blocks)
    print('first hash:{}'.format(result[0]))

if __name__ == '__main__':
    run('./files/real')
