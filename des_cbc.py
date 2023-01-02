import math
import os
import random
import binascii
from textwrap import wrap


# -------------------------------- Tables  -------------------------------- #
#Holds permutation instructions to generate 56bit key from 64bit key
#(equivalent to P10 in lab manual)
parity_drop_table = [56, 48, 40, 32, 24, 16, 8,
       0, 57, 49, 41, 33, 25, 17,
       9, 1, 58, 50, 42, 34, 26,
       18, 10, 2, 59, 51, 43, 35,
       62, 54, 46, 38, 30, 22, 14,
       6, 61, 53, 45, 37, 29, 21,
       13, 5, 60, 52, 44, 36, 28,
       20, 12, 4, 27, 19, 11, 3
       ]

#compression permutation table (equivalent to P8 in lab manual)
#used to generate 48bit key from 56bit key
compression_Dbox = [13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]


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



# -------------------------------- Functions  -------------------------------- #

def generate_keys(key64):
    #step 1: Generate 56 bit key from 64 bit key using parity drop table
    #convert key64 to string
    print("KEY BINARY",key64)
    key56 = [key64[parity_drop_table[i]] for i in range(56)]

    #step 2: Split key into two halves
    key_half1 = key56[:28]
    key_half2 = key56[28:]

    #step 3: Generate 16 keys
    keys = []
    for i in range(16):
        #step 4: left shift by 1 or 2 depending on round
        key_half1 = key_half1[1:] + key_half1[:1]
        key_half2 = key_half2[1:] + key_half2[:1]

        #if we're in round 1, 2, 9, 16 then we left shift by 2 (according to textbook)
        if i not in [0, 1, 8, 15]:
            key_half1 = key_half1[1:] + key_half1[:1]
            key_half2 = key_half2[1:] + key_half2[:1]

        #step 5: Combine left and right and apply compression permutation
        combined = key_half1 + key_half2
        key = [combined[compression_Dbox[i]] for i in range(48)]
        #convert list to string
        key = ''.join(key)
        keys.append(key)

    return keys


def encrypt_DES(bin_text, key):
    keys = generate_keys(key)
    #start the encryption process

    # Initial Permutation
    permuted_text = permutation(bin_text, initial_permutation_table)

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
    concatenate_text = xor_result_bin+lpt
    cipher_text = permutation(
        concatenate_text, final_permutation_table)
    return cipher_text

def decrypt_DES(bin_text, key):
    keys = generate_keys(key)
    #start the decryption process

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

    concatenate_text = xor_result_bin+lpt
    plaintext = permutation(
            concatenate_text, final_permutation_table)
    return plaintext


def encrypt_CBC(message_bin, iv_binary, key):
    # NUMBER OF BLOCKS
    # Calculate the number of 64 bit blocks 
    # // is used to floor the number or convert it from float to integer
    no_of_blocks = len(message_bin)//64 

    # CBC ENCRYPTION
    # The IV is considered as the initial ciphertext block used for the first XOR operation
    ciphertext_block = iv_binary

    ciphertext_bin = ""
    
    for i in range(no_of_blocks):

        # XOR of the ith block of message (e.g. from bit 0 to bit 64)
        # with the previous ciphertext block
        xor_result = int(message_bin[i*64:(i+1)*64], 2) ^ int(''.join([str(bits) for bits in ciphertext_block]), 2)

        # The result is converted to binary, the first two characters "0b" are removed,
        # and if there were 0s at the beginning of the number that were removed they will be filled with zfill
        xor_result_bin = bin(xor_result)[2:].zfill(64) 

        # The result is encrypted wusing the DES encryption
        ciphertext_block = encrypt_DES(xor_result_bin, key)

        # The result is also concatenated to the ciphertext
        ciphertext_bin += ''.join([str(bits) for bits in ciphertext_block])

    return ciphertext_bin


def decrypt_CBC(ciphertext_bin, iv_binary, key):
    # NUMBER OF BLOCKS
    # Calculate the number of 64 bit blocks 
    # // is used to floor the number or convert it from float to integer
    no_of_blocks = len(ciphertext_bin)//64

    # CBC DECRYPTION
    # The IV is the first block used before the first ciphertext block
    prev_block = iv_binary
    
    message_bin = ""


    for i in range(no_of_blocks):

        # Get the current block of ciphertext (e.g. from bit 0 to bit 64)
        curr_block = ciphertext_bin[i*64:(i+1)*64]

        # Decrypt it using the DES decryption
        des_decrypted = decrypt_DES(curr_block, key)

        # XOR the decrypted block with the previous ciphertext block
        xor_result = int(''.join([str(bits) for bits in des_decrypted]), 2) ^ int(''.join([str(bits) for bits in prev_block]), 2)
        
        # The result is converted to binary, the first two characters "0b" are removed,
        # and if there were 0s at the beginning of the number that were removed they will be filled with zfill
        xor_result_bin = bin(xor_result)[2:].zfill(64) 
        
        # The result is concatenated to the decrypted message
        message_bin += xor_result_bin
        
        prev_block = curr_block

    return message_bin



def get_sbox_value(row, col, sbox_num):
    value = sboxes[sbox_num][row][col]
    return format(value, '04b')


def permutation(bin_text, table):
    return [bin_text[i-1] for i in table]


# ------------------------------- ROOT FUNCTIONS ------------------------------- #
# ------------------ ENCRYPT ------------------ #
def encrypt(message, message_type, key, key_type, iv, iv_type, cipherBox):
    message = message.get().replace(' ', '')
    message_type = message_type.get()
    '''
    message = "helloworldhellow"
    message_type = 1
    '''
    key = key.get().replace(' ', '')
    key_type = key_type.get()
    '''
    key = "0101101001011010010111001001101001011010010110100101101001011010"
    key_type = 3
    '''
    iv = iv.get().replace(' ', '')
    iv_type = iv_type.get()
    '''
    # Generate a random number that is suitable for cryptographic use
    # TODO: Make sure that urandom is safe to use and know why (PRNG, etc...)
    # CONVERT THE INITIAL VALUE FROM BYTES TO BINARY
    # Convert the IV from bytes to integer ("big" indicates that the MSB is at the start)
    # Convert the IV from integer to binary
    iv_binary = os.urandom(8).bin(int.from_bytes(iv, "big"))    
    '''
    cipher=""
    # ----- MESSAGE CONVERSIONS ----- #
    if(message_type == 1):
        # CONVERT THE STRING TO BINARY
        # Convert each character to its ASCII equivilant with the ord() function
        # Convert the integer into a binary number and join it with the previous characters with format() and join()
        message_bin = ''.join(format(ord(i), '08b') for i in message)
    elif(message_type == 2):
        # CONVERT THE HEX TO BINARY
        message_bin = "{0:08b}".format(int(message, 16))
    elif(message_type ==3):
        message_bin = message

    # ----- KEY CONVERSIONS ----- #
    if(key_type == 1):
        key_bin = ''.join(format(ord(i), '08b') for i in key)
    elif(key_type == 2):
        key_bin = "{0:08b}".format(int(key, 16))
    elif(key_type ==3):
        key_bin = key

    # ----- IV CONVERSIONS ----- #
    if(iv_type == 1):
        iv_binary = ''.join(format(ord(i), '08b') for i in iv)
    elif(iv_type == 2):
        iv_binary = "{0:08b}".format(int(iv, 16))
    elif(iv_type ==3):
        iv_binary = iv

    # ----- PKCS7 PADDING ----- #
    block_size=64
    no_of_blocks = math.ceil(len(message_bin)/float(block_size))
    pad_value = int(no_of_blocks * block_size - len(message_bin))
    # print(pad_value)
    if pad_value == 0:
       message_bin = message_bin + chr(block_size) * block_size
    else:
        message_bin = message_bin + chr(pad_value) * pad_value
    # ------------------- #

    cipher_bin = encrypt_CBC(message_bin, iv_binary, key_bin)

    # ----- CONVERT CIPHER BACK TO MATCH MESSAGE TYPE ----- #
    if(message_type == 1):
        # CONVERT FROM BINARY TO STRING
        cipher = ''.join(chr(int(cipher_bin[i:i+8],2)) for i in range(0,len(cipher_bin),8))
        # cipher = int('0b'+cipher_bin, 2).to_bytes((int('0b'+cipher_bin, 2).bit_length()+7) // 8, 'big').decode()
    elif(message_type == 2):
        # CONVERT FROM BINARY TO HEX
        cipher = '%0*X' % ((len(cipher_bin) + 3) // 4, int(cipher_bin, 2))
    elif(message_type == 3):
        cipher = cipher_bin


    # ----- CONSOLE DISPLAYS ----- #

    print("MESSAGE BINARY: ", message_bin)    
    '''
    #Key Generation Test
    print("-------------------------")
    print("Key Generation Test")
    print("-------------------------")
    print("Input Key: ", key_bin)
    print("Generated Keys: " )
    keys = generate_keys(key_bin)
    for i in range(16):
        print("Round " + str(i+1) + ": ", end = "")
        print(keys[i])
    '''
    print("ENCRYPTED BINARY: ", cipher_bin)
    print("ENCRYPTED:", cipher)

    
    cipherBox['text'] = cipher



# ------------------ DECRYPT ------------------ #

def decrypt(cipher, cipher_type, key, key_type, iv, iv_type, messageBox):
    cipher = cipher.get().replace(' ', '')
    cipher_type = cipher_type.get()
   
    key = key.get().replace(' ', '')
    key_type = key_type.get()
   
    iv = iv.get().replace(' ', '')
    iv_type = iv_type.get()

    message=""

    # ----- CIPHER CONVERSIONS ----- #
    if(cipher_type == 1):
       cipher_bin = ''.join(format(ord(i), '08b') for i in cipher)
    elif(cipher_type == 2):
        cipher_bin = "{0:08b}".format(int(cipher, 16))
    elif(cipher_type ==3):
        cipher_bin = cipher

    # ----- KEY CONVERSIONS ----- #
    if(key_type == 1):
        key_bin = ''.join(format(ord(i), '08b') for i in key)
    elif(key_type == 2):
        key_bin = "{0:08b}".format(int(key, 16))
    elif(key_type ==3):
        key_bin = key

    # ----- IV CONVERSIONS ----- #
    if(iv_type == 1):
        iv_binary = ''.join(format(ord(i), '08b') for i in iv)
    elif(iv_type == 2):
        iv_binary = "{0:08b}".format(int(iv, 16))
    elif(iv_type ==3):
        iv_binary = iv

# TODO: figure if needed at all? if yes, remove padding? add padding?
    # # ----- PKCS7 PADDING ----- #
    # block_size=64
    # no_of_blocks = math.ceil(len(cipher_bin)/float(block_size))
    # pad_value = int(no_of_blocks * block_size - len(cipher_bin))
    # if pad_value == 0:
    #    cipher_bin = cipher_bin + chr(block_size) * block_size
    # else:
    #     cipher_bin = cipher_bin + chr(pad_value) * pad_value
    # # ------------------- #

    message_bin = decrypt_CBC(cipher_bin, iv_binary, key_bin)

    # ----- CONVERT CIPHER BACK TO MATCH CIPHER TYPE ----- #
    if(cipher_type == 1):
        message = ''.join(chr(int(message_bin[i:i+8],2)) for i in range(0,len(message_bin),8))
    elif(cipher_type == 2):
        message = '%0*X' % ((len(message_bin) + 3) // 4, int(message_bin, 2))
    elif(cipher_type == 3):
        message = message_bin


    # ----- CONSOLE DISPLAYS ----- #

    print("CIPHER BINARY: ", cipher_bin)    
    '''
    #Key Generation Test
    print("-------------------------")
    print("Key Generation Test")
    print("-------------------------")
    print("Input Key: ", key_bin)
    print("Generated Keys: " )
    keys = generate_keys(key_bin)
    for i in range(16):
        print("Round " + str(i+1) + ": ", end = "")
        print(keys[i])
    '''
    print("DECRYPTED BINARY: ", message_bin)
    print("DECRYPTED: ", message)

    messageBox['text'] = message

