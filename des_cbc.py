import os
import random

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
copmression_Dbox = [13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]

def encrypt(message, key, initVector, cipherBox):
    message = message.get().upper()
    key = int(key.get())
    initVector = initVector.get().upper()
    cipher = ""

    cipher = "yet to be implemented"

    cipherBox['text'] = cipher

    # TODO: Integrate the CBC and DES ciphers

def decrypt(cipher, key, initVector, messageBox):
    cipher = cipher.get().upper()
    key = int(key.get())
    initVector = initVector.get().upper()
    message = ""

    message = "yet to be implemented"

    messageBox['text'] = message

def generate_keys(key64):
    #step 1: Generate 56 bit key from 64 bit key using parity drop table
    #convert key64 to string
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
        key = [combined[copmression_Dbox[i]] for i in range(48)]
        #convert list to string
        key = ''.join(key)
        keys.append(key)

    return keys


def encrypt_DES(bin_text, key):
    keys = generate_keys(key)
    #start the encryption process
   

    return bin_text

def decrypt_DES(text, key):
    keys = generate_keys(key)
    #start the decryption process


    return text


def encrypt_CBC(plaintext, iv, key):
    
    # CONVERT THE INITIAL VALUE FROM BYTES TO BINARY
    # Convert the IV from bytes to integer ("big" indicates that the MSB is at the start)
    # Convert the IV from integer to binary
    iv_binary = bin(int.from_bytes(iv, "big"))
    
    # CONVERT THE PLAINTEXT STRING TO BINARY
    # Convert each character to its ASCII equivilant with the ord() function
    # Convert the integer into a binary number and join it with the previous characters with format() and join()
    plaintext_bin = ''.join(format(ord(i), '08b') for i in plaintext)

    # PADDING THE BINARY PLAINTEXT
    # TODO: implement padding for when the plaintext length is not a multiple of 64 

    # NUMBER OF BLOCKS
    # Calculate the number of 64 bit blocks 
    # // is used to floor the number or convert it from float to integer
    no_of_blocks = len(plaintext_bin)//64 

    # CBC ENCRYPTION
    # The IV is considered as the initial ciphertext block used for the first XOR operation
    ciphertext_block = iv_binary

    ciphertext_bin = ""
    
    for i in range(no_of_blocks):

        # XOR of the ith block of plaintext (e.g. from bit 0 to bit 64)
        # with the previous ciphertext block
        xor_result = int(plaintext_bin[i*64:(i+1)*64], 2) ^ int(ciphertext_block, 2)

        # The result is converted to binary, the first two characters "0b" are removed,
        # and if there were 0s at the beginning of the number that were removed they will be filled with zfill
        xor_result_bin = bin(xor_result)[2:].zfill(64) 

        # The result is encrypted wusing the DES encryption
        ciphertext_block = encrypt_DES(xor_result_bin, key)

        # The result is also concatenated to the ciphertext
        ciphertext_bin += ciphertext_block

    # TODO: Convert the binary ciphertext into characters
    return ciphertext_bin


def decrypt_CBC(ciphertext, iv, key):
    
    # CONVERT THE INITIAL VALUE FROM BYTES TO BINARY
    # Convert the IV from bytes to integer ("big" indicates that the MSB is at the start)
    # Convert the IV from integer to binary
    iv_binary = bin(int.from_bytes(iv, "big"))

    # CONVERT THE CIPHERTEXT STRING TO BINARY
    # Convert each character to its ASCII equivilant with the ord() function
    # Convert the integer into a binary number and join it with the previous characters with format() and join()
    # ciphertext_bin = ''.join(format(ord(i), '08b') for i in ciphertext)
    ciphertext_bin = ciphertext

    # PADDING?
    # TODO: Not sure if this could be needed

    # NUMBER OF BLOCKS
    # Calculate the number of 64 bit blocks 
    # // is used to floor the number or convert it from float to integer
    no_of_blocks = len(ciphertext_bin)//64

    # CBC DECRYPTION
    # The IV is the first block used before the first ciphertext block
    prev_block = iv_binary
    
    plaintext_bin = ""


    for i in range(no_of_blocks):

        # Get the current block of ciphertext (e.g. from bit 0 to bit 64)
        curr_block = ciphertext_bin[i*64:(i+1)*64]

        # Decrypt it using the DES decryption
        des_decrypted = decrypt_DES(curr_block, key)

        # XOR the decrypted block with the previous ciphertext block
        xor_result = int(des_decrypted, 2) ^ int(prev_block, 2)
        
        # The result is converted to binary, the first two characters "0b" are removed,
        # and if there were 0s at the beginning of the number that were removed they will be filled with zfill
        xor_result_bin = bin(xor_result)[2:].zfill(64) 
        
        # The result is concatenated to the decrypted plaintext
        plaintext_bin += xor_result_bin
        
        prev_block = curr_block

    # TODO: Convert the binary plaintext into characters
    return plaintext_bin



#-----------------------MAIN-----------------------#
#sample key input
key = "0101101001011010010110100101101001011010010110100101101001011010010110100101101001011010010110100101101001011010"

# Generate a random number that is suitable for cryptographic use
# TODO: Make sure that urandom is safe to use and know why (PRNG, etc...)
iv = os.urandom(8)

# NOTE: This string's length is divisible by 64 so it works
plaintext = "helloworldhellow"

encrypted = encrypt_CBC(plaintext, iv, key)
print("ENCRYPTED: ", encrypted)

decrypted = decrypt_CBC(encrypted, iv, key)
print("DECRYPTED: ", decrypted)

# For comparison only, we display the plaintext in binary
print("PLAINTEXT: ", ''.join(format(ord(i), '08b') for i in plaintext))

#Key Generation Test
print("-------------------------")
print("Key Generation Test")
print("-------------------------")
print("Input Key: ", key)
print("Generated Keys: " )
keys = generate_keys(key)
for i in range(16):
    print("Round " + str(i+1) + ": ", end = "")
    print(keys[i])