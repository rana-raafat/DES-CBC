initial_permutation_table = [58, 50, 42, 34, 26, 18, 10, 2,	60,	52,	44,	36,	28,	20,	12,	4,
                             62, 54, 46, 38, 30, 22, 14, 6,	64,	56,	48,	40,	32,	24,	16,	8,
                             57, 49, 41, 33, 25, 17, 9,	1, 59, 51,	43,	35,	27,	19,	11,	3,
                             61, 53, 45, 37, 29, 21, 13, 5,	63,	55,	47,	39,	31,	23,	15,	7
                             ]
final_permutation_table = [40, 8, 48, 16, 56, 24, 64, 32,
                           39, 7, 47, 15, 55, 23, 63, 31,
                           38, 6, 46, 14, 54, 22, 62, 30,
                           37, 5, 45, 13, 53, 21, 61, 29,
                           36, 4, 44, 12, 52, 20, 60, 28,
                           35, 3, 43, 11, 51, 19, 59, 27,
                           34, 2, 42, 10, 50, 18, 58, 26,
                           33, 1, 41, 9, 49, 17, 57, 25]
end_of_round_permutation_table = [16, 7, 20, 21, 29, 12, 28, 17,
                                  1, 15, 23, 26, 5, 18, 31, 10,
                                  2, 8, 24, 14, 32, 27, 3, 9,
                                  19, 13, 30, 6, 22, 11, 4, 25]
expansion_permutation_table = [32, 1, 2, 3, 4, 5,
                               4, 5, 6, 7, 8, 9,
                               8, 9, 10, 11, 12, 13,
                               12, 13, 14, 15, 16, 17,
                               16, 17, 18, 19, 20, 21,
                               20, 21, 22, 23, 24, 25,
                               24, 25, 26, 27, 28, 29,
                               28, 29, 31, 31, 32, 1]
parity_drop_table = [56, 48, 40, 32, 24, 16, 8,
                     0, 57, 49, 41, 33, 25, 17,
                     9, 1, 58, 50, 42, 34, 26,
                     18, 10, 2, 59, 51, 43, 35,
                     62, 54, 46, 38, 30, 22, 14,
                     6, 61, 53, 45, 37, 29, 21,
                     13, 5, 60, 52, 44, 36, 28,
                     20, 12, 4, 27, 19, 11, 3
                     ]

# compression permutation table (equivalent to P8 in lab manual)
# used to generate 48bit key from 56bit key
copmression_Dbox = [13, 16, 10, 23, 0, 4,
                    2, 27, 14, 5, 20, 9,
                    22, 18, 11, 3, 25, 7,
                    15, 6, 26, 19, 12, 1,
                    40, 51, 30, 36, 46, 54,
                    29, 39, 50, 44, 32, 47,
                    43, 48, 38, 55, 33, 52,
                    45, 41, 49, 35, 28, 31
                    ]
# array of 8 sboxes to use in sbox permutation
sboxes = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, ],
     [0, 15, 7, 4, 14, 2, 13, 10, 3, 6, 12, 11, 9, 5, 3, 8, ],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, ],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, ],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, ],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, ],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, ],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, ],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, ],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, ],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9, ],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, ],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, ],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, ],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, ],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, ], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, ],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, ],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 10, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 00, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, ],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, ],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, ],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, ],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 10, 14, 9, 2, ],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 10, 15, 3, 5, 8, ],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 9, 3, 5, 6, 11]]
]

key = "0101101001011010010110100101101001011010010110100101101001011010010110100101101001011010010110100101101001011010"


def generate_keys(key64):
    # step 1: Generate 56 bit key from 64 bit key using parity drop table
    # convert key64 to string
    key56 = [key64[parity_drop_table[i]] for i in range(56)]

    # step 2: Split key into two halves
    key_half1 = key56[:28]
    key_half2 = key56[28:]

    # step 3: Generate 16 keys
    keys = []
    for i in range(16):
        # step 4: left shift by 1 or 2 depending on round
        key_half1 = key_half1[1:] + key_half1[:1]
        key_half2 = key_half2[1:] + key_half2[:1]

        # if we're in round 1, 2, 9, 16 then we left shift by 2 (according to textbook)
        if i not in [0, 1, 8, 15]:
            key_half1 = key_half1[1:] + key_half1[:1]
            key_half2 = key_half2[1:] + key_half2[:1]

        # step 5: Combine left and right and apply compression permutation
        combined = key_half1 + key_half2
        key = [combined[copmression_Dbox[i]] for i in range(48)]
        # convert list to string
        key = ''.join(key)
        keys.append(key)

    return keys


def encrypt_DES(plain_text, key):
    keys = generate_keys(key)
    # start the encryption process

    # convet text into binary
    plaintext_bin = ''.join(format(ord(i), '08b') for i in plain_text)

    # Get number of blocks
    no_of_blocks = len(plaintext_bin)//64

    permuted_text = ""
    ciphertext = ""
    # loop to apply round on each 64 bit block
    for i in range(no_of_blocks):
        bin_text = plaintext_bin[i*64:(i+1)*64]

        # Initial Permutation
        permuted_text = permutation(bin_text, initial_permutation_table)
        # print(permuted_text)
        # divide each 64 bit block into 2 halves --> lpt (Left Plain text) and rpt (right plain text)
        lpt, rpt = permuted_text[:len(
            permuted_text)//2], permuted_text[len(permuted_text)//2:]

        for j in range(16):

            # expansion permutation --> RPT is expanded from 32 bits to 48 bits
            expanded_RPT = permutation(rpt, expansion_permutation_table)

            # XOR right section and the round key
            xor_result = int(
                ''.join([str(bits) for bits in expanded_RPT]), 2) ^ int(keys[j], 2)
            xor_result_bin = format(xor_result, '048b')

            # Divide into 8 blocks
            block1, block2, block3, block4, block5, block6, block7, block8 = [
                xor_result_bin[i:i+6] for i in range(0, len(xor_result_bin), 6)]
            blocks = [block1, block2, block3, block4,
                      block5, block6, block7, block8]

            sbox_num = 0
            s_box_ouput = ""
            # Sbox from 6 bits to 4 bits
            for block in blocks:
                row = block[0]+block[5]
                col = block[1]+block[2]+block[3]+block[4]

                # concatenate into 32 bits
                s_box_ouput += get_sbox_value(int(row, 2),
                                              int(col, 2), sbox_num)
                sbox_num += 1

            end_of_round_permutation = permutation(
                s_box_ouput, end_of_round_permutation_table)

            xor_result = int(''.join([str(bits) for bits in lpt]), 2) ^ int(
                ''.join([str(bits) for bits in end_of_round_permutation]), 2)
            xor_result_bin = format(xor_result, '032b')
            temp = rpt
            rpt = xor_result_bin
            lpt = ''.join([str(bits) for bits in temp])

    # final permutation
        concatenate_text = lpt+xor_result_bin
        finalciphertext = ciphertext.join([str(bits) for bits in permutation(
            concatenate_text, final_permutation_table)])
    return finalciphertext


def decrypt_DES(cipher_text, key):
    keys = generate_keys(key)
    # start the encryption process

    # convet text into binary
    # plaintext_bin = ''.join(format(ord(i), '08b') for i in plain_text)
    # Get number of blocks
    no_of_blocks = len(cipher_text)//64

    permuted_text = ""
    ciphertext = ""
    # loop to apply round on each 64 bit block
    for i in range(no_of_blocks):

        bin_text = cipher_text[i*64:(i+1)*64]

        # Initial Permutation
        permuted_text = permutation(bin_text, initial_permutation_table)

        # divide each 64 bit block into 2 halves --> lpt (Left Plain text) and rpt (right plain text)
        lpt, rpt = permuted_text[:len(
            permuted_text)//2], permuted_text[len(permuted_text)//2:]

        for j in reversed(range(16)):

            # expansion permutation --> RPT is expanded from 32 bits to 48 bits
            expanded_RPT = permutation(rpt, expansion_permutation_table)

            # XOR right section and the round key
            xor_result = int(
                ''.join([str(bits) for bits in expanded_RPT]), 2) ^ int(keys[j], 2)
            xor_result_bin = format(xor_result, '048b')

            # Divide into 8 blocks
            block1, block2, block3, block4, block5, block6, block7, block8 = [
                xor_result_bin[i:i+6] for i in range(0, len(xor_result_bin), 6)]
            blocks = [block1, block2, block3, block4,
                      block5, block6, block7, block8]

            sbox_num = 0
            s_box_ouput = ""
            # Sbox from 6 bits to 4 bits
            for block in blocks:
                row = block[0]+block[5]
                col = block[1]+block[2]+block[3]+block[4]

                # concatenate into 32 bits
                s_box_ouput += get_sbox_value(int(row, 2),
                                              int(col, 2), sbox_num)
                sbox_num += 1

            end_of_round_permutation = permutation(
                s_box_ouput, end_of_round_permutation_table)

            xor_result = int(''.join([str(bits) for bits in lpt]), 2) ^ int(
                ''.join([str(bits) for bits in end_of_round_permutation]), 2)
            xor_result_bin = format(xor_result, '032b')
            temp = rpt
            rpt = xor_result_bin
            lpt = ''.join([str(bits) for bits in temp])

    # final permutation
        concatenate_text = lpt+xor_result_bin
        finalciphertext = ciphertext.join([str(bits) for bits in permutation(
            concatenate_text, final_permutation_table)])
    return finalciphertext


def get_sbox_value(row, col, sbox_num):
    value = sboxes[sbox_num][row][col]
    return format(value, '04b')


def permutation(bin_text, table):
    return [bin_text[i-1] for i in table]


print("plain text")
print(''.join(format(ord(i), '08b') for i in "hellowor"))
print("encrypted text")
print(''.join([str(bits) for bits in encrypt_DES("hellowor", key)]))

# print(len(''.join([str(bits)
#       for bits in encrypt_DES("hellowor", key)])))
print("decrypted text")
print(decrypt_DES(''.join([str(bits)
      for bits in encrypt_DES("hellowor", key)]), key))
# print(len(decrypt_DES(''.join([str(bits)
#       for bits in encrypt_DES("helloworldhellow", key)]), key)))

# print(decrypt_DES("helloworldhellow", key))
