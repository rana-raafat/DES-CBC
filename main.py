from tkinter import *
import tkinter.ttk as ttk

from des_cbc import encrypt, decrypt

def main():
    window = Tk()
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    window.geometry("%dx%d" % (screenWidth, screenHeight))
    window.configure(background='#1C1C1C')
    style = ttk.Style(window)
    style.theme_use('clam')

    # --------------------------------------------------- Labels --------------------------------------------------- #

    name = Label(text='Function: Data Encryption Standard (DES)')
    name.configure(background='#1C1C1C', font=30, fg='white')
    name.pack(pady=15, side=TOP, anchor="center")

    id = Label(text='Mode: Cipher Block Chaining (CBC) ')
    id.configure(background='#1C1C1C', font=30, fg='white')
    id.pack(pady=15, side=TOP, anchor="center")

    separator1 = ttk.Separator(window, orient='horizontal')
    separator1.pack(pady=30, fill='x')

    #--------------------------------------------------- Encryption --------------------------------------------------- #

    enc_message = StringVar()

    enc_messageLabel = Label(text='Enter plaintext:')
    enc_messageLabel.configure(background='#1C1C1C', font=50, fg='white')
    enc_messageLabel.place(x=25, y=160)

    enc_messageBox = ttk.Entry(window, width=125,  font=50, textvariable=enc_message)
    enc_messageBox.place(x=215, y=160)

    enc_key = StringVar()

    enc_keyLabel = Label(text='Enter key:')
    enc_keyLabel.configure(background='#1C1C1C', font=50, fg='white')
    enc_keyLabel.place(x=25, y=220)

    enc_keyBox = ttk.Entry(window, width=125,  font=50, textvariable=enc_key)
    enc_keyBox.place(x=215, y=220)

    enc_initVector = StringVar()

    enc_initVectorLabel = Label(text='Enter Initialization Vector:')
    enc_initVectorLabel.configure(background='#1C1C1C', font=50, fg='white')
    enc_initVectorLabel.place(x=25, y=280)

    enc_initVectorBox = ttk.Entry(window, width=125,  font=50, textvariable=enc_initVector)
    enc_initVectorBox.place(x=215, y=280)

    enc_cipherLabel = Label(text='Resulting ciphertext:')
    enc_cipherLabel.configure(background='#1C1C1C', font=50, fg='white')
    enc_cipherLabel.place(x=25, y=340)

    enc_cipherBox = Label()
    enc_cipherBox.configure(background='#FFFFFF', width=125,  font=50, fg='red')
    enc_cipherBox.place(x=215, y=340)

    enc_encyptionButton = ttk.Button(window,
                           text='Encrypt',
                           command=lambda: encrypt(enc_message, enc_key, enc_initVector, enc_cipherBox))
    enc_encyptionButton.place(x=725, y=380)

    separator2 = ttk.Separator(window, orient='horizontal')
    separator2.place(x=0, y=screenHeight/2, width=screenWidth)


    # --------------------------------------------------- Decryption --------------------------------------------------- #

    dec_cipher = StringVar()

    dec_cipherLabel = Label(text='Enter ciphertext:')
    dec_cipherLabel.configure(background='#1C1C1C', font=50, fg='white')
    dec_cipherLabel.place(x=25, y=460)

    dec_cipherBox = ttk.Entry(window, width=125, font=50, textvariable=dec_cipher)
    dec_cipherBox.place(x=215, y=460)

    dec_key = StringVar()

    dec_keyLabel = Label(text='Enter key:')
    dec_keyLabel.configure(background='#1C1C1C', font=50, fg='white')
    dec_keyLabel.place(x=25, y=520)

    dec_keyBox = ttk.Entry(window, width=125,  font=50, textvariable=dec_key)
    dec_keyBox.place(x=215, y=520)

    dec_initVector = StringVar()

    dec_initVectorLabel = Label(text='Enter Initialization Vector:')
    dec_initVectorLabel.configure(background='#1C1C1C', font=50, fg='white')
    dec_initVectorLabel.place(x=25, y=580)

    dec_initVectorBox = ttk.Entry(window, width=125, font=50, textvariable=dec_initVector)
    dec_initVectorBox.place(x=215, y=580)

    dec_messageLabel = Label(text='Resulting plaintext:')
    dec_messageLabel.configure(background='#1C1C1C', font=50, fg='white')
    dec_messageLabel.place(x=25, y=640)

    dec_messageBox = Label()
    dec_messageBox.configure(background='#FFFFFF', width=125,  font=50, fg='red')
    dec_messageBox.pack(anchor="w")

    dec_messageBox.place(x=215, y=640)

    dec_caesarButton = ttk.Button(window,
                                  text='Decrypt',
                                  command=lambda: decrypt(dec_cipher, dec_key, dec_initVector, dec_messageBox))
    dec_caesarButton.place(x=725, y=680)

    # ---------------------------------------------------------------------------------------------------------------- #

    window.mainloop()

main()