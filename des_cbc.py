import os

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


def encrypt_DES(text):
    return text

def decrypt_DES(text):
    return text


def encrypt_CBC(plaintext, iv):
    
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
        ciphertext_block = encrypt_DES(xor_result_bin)

        # The result is also concatenated to the ciphertext
        ciphertext_bin += ciphertext_block

    # TODO: Convert the binary ciphertext into characters
    return ciphertext_bin


def decrypt_CBC(ciphertext, iv):
    
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
        des_decrypted = decrypt_DES(curr_block)

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


# Generate a random number that is suitable for cryptographic use
# TODO: Make sure that urandom is safe to use and know why (PRNG, etc...)
iv = os.urandom(8)

# NOTE: This string's length is divisible by 64 so it works
plaintext = "helloworldhellow"

encrypted = encrypt_CBC(plaintext, iv)
print("ENCRYPTED: ", encrypted)

decrypted = decrypt_CBC(encrypted, iv)
print("DECRYPTED: ", decrypted)

# For comparison only, we display the plaintext in binary
print("PLAINTEXT: ", ''.join(format(ord(i), '08b') for i in plaintext))