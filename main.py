from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as font
from des_cbc import encrypt, decrypt

def character_limit(entry_text, entry_type):
    if len(entry_text.get()) > 0:
        if(entry_type.get() == 1):
            entry_text.set(entry_text.get().replace(' ', '')[:8])
        elif(entry_type.get() == 2):
            entry_text.set(entry_text.get().replace(' ', '')[:16])
        elif(entry_type.get() == 3):
            entry_text.set(entry_text.get().replace(' ', '')[:64])

def main():
    window = Tk()
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    window.geometry("%dx%d" % (screenWidth, screenHeight))
    window.configure(background='#1C1C1C')
    style = ttk.Style(window)
    style.theme_use('clam')

    # ------------------------------- Title ------------------------------- #

    name = Label(text='Function: Data Encryption Standard (DES)')
    name.configure(background='#1C1C1C', font=30, fg='white')
    name.pack(padx=15, pady=15, side=LEFT, anchor="nw")

    id = Label(text='Mode: Cipher Block Chaining (CBC) ')
    id.configure(background='#1C1C1C', font=30, fg='white')
    id.pack(padx=15, pady=15, side=RIGHT, anchor="ne")

    separator1 = ttk.Separator(window, orient='horizontal')
    separator1.pack(pady=30, fill='x')
    
    separator2 = ttk.Separator(window, orient='horizontal')
    separator2.place(x=0, y=60, width=screenWidth)


    # ------------------------------- Encryption ------------------------------- #
    # --------- Message --------- #
    enc_message = StringVar()

    enc_messageLabel = Label(text='Enter Message:')
    enc_messageLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    enc_messageLabel.place(x=25, y=100)

    enc_messageBox = ttk.Entry(window, width=115,  font=50, textvariable=enc_message)
    enc_messageBox.place(x=225, y=100)

    enc_message_type = IntVar(None, 1)

    E11 = Radiobutton(window, text="plaintext", value=1, variable=enc_message_type)
    E11.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E11['font']= font.Font(family='Helvetica', size=11)
    E11.place(x=1200, y=130)

    E12 = Radiobutton(window, text="hexidecimal", value=2, variable=enc_message_type)
    E12.configure(background='#1C1C1C', activebackground='#1C1C1C', foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E12['font']= font.Font(family='Helvetica', size=11)
    E12.place(x=1300, y=130)

    E13 = Radiobutton(window, text="binary", value=3, variable=enc_message_type)
    E13.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E13['font']= font.Font(family='Helvetica', size=11)
    E13.place(x=1420, y=130)

    # --------- Key --------- #
    
    enc_key = StringVar()
    
    enc_keyLabel = Label(text='Enter Key:')
    enc_keyLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    enc_keyLabel.place(x=25, y=170)

    enc_keyBox = ttk.Entry(window, width=115,  font=50, textvariable=enc_key)
    enc_keyBox.place(x=225, y=170)

    enc_key_type = IntVar(None, 1)

    E21 = Radiobutton(window, text="plaintext", value=1, variable=enc_key_type)
    E21.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E21['font']= font.Font(family='Helvetica', size=11)
    E21.place(x=1200, y=200)

    E22 = Radiobutton(window, text="hexidecimal", value=2, variable=enc_key_type)
    E22.configure(background='#1C1C1C', activebackground='#1C1C1C', foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E22['font']= font.Font(family='Helvetica', size=11)
    E22.place(x=1300, y=200)

    E23 = Radiobutton(window, text="binary", value=3, variable=enc_key_type)
    E23.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E23['font']= font.Font(family='Helvetica', size=11)
    E23.place(x=1420, y=200)

    enc_key.trace("w", lambda *args: character_limit(enc_key, enc_key_type))

    # --------- IV --------- #

    enc_initVector = StringVar()
    
    enc_initVectorLabel = Label(text='Enter Initialization Vector:')
    enc_initVectorLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    enc_initVectorLabel.place(x=25, y=230)

    enc_initVectorBox = ttk.Entry(window, width=115,  font=50, textvariable=enc_initVector)
    enc_initVectorBox.place(x=225, y=240)

    enc_initVector_type = IntVar(None, 1)

    E31 = Radiobutton(window, text="plaintext", value=1, variable=enc_initVector_type)
    E31.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E31['font']= font.Font(family='Helvetica', size=11)
    E31.place(x=1200, y=270)

    E32 = Radiobutton(window, text="hexidecimal", value=2, variable=enc_initVector_type)
    E32.configure(background='#1C1C1C', activebackground='#1C1C1C', foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E32['font']= font.Font(family='Helvetica', size=11)
    E32.place(x=1300, y=270)

    E33 = Radiobutton(window, text="binary", value=3, variable=enc_initVector_type)
    E33.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    E33['font']= font.Font(family='Helvetica', size=11)
    E33.place(x=1420, y=270)

    enc_initVector.trace("w", lambda *args: character_limit(enc_initVector, enc_initVector_type))

    # --------- Result --------- #

    enc_cipherLabel = Label(text='Resulting Ciphertext:')
    enc_cipherLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    enc_cipherLabel.place(x=25, y=310)

    enc_cipherBox = Label()
    enc_cipherBox.configure(background='#FFFFFF', width=115, height=1, font=50, fg='red', justify='left', wraplengt=1250)
    enc_cipherBox.place(x=225, y=310)

    # --------- Button --------- #

    enc_encyptionButton = ttk.Button(window,
                           text='Encrypt',
                           command=lambda: encrypt(enc_message, enc_message_type, enc_key, enc_key_type, enc_initVector, enc_initVector_type, enc_cipherBox))
    enc_encyptionButton.place(x=725, y=360)

    # -------------------------- #

    separator2 = ttk.Separator(window, orient='horizontal')
    separator2.place(x=0, y=425, width=screenWidth)


    # ------------------------------- Decryption ------------------------------- #
    # --------- Message --------- #
    dec_cipher = StringVar()

    dec_cipherLabel = Label(text='Enter Cipher:')
    dec_cipherLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    dec_cipherLabel.place(x=25, y=470)

    dec_cipherBox = ttk.Entry(window, width=115, font=50, textvariable=dec_cipher)
    dec_cipherBox.place(x=225, y=470)

    dec_cipher_type = IntVar(None, 1)

    D11 = Radiobutton(window, text="plaintext", value=1, variable=dec_cipher_type)
    D11.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D11['font']= font.Font(family='Helvetica', size=11)
    D11.place(x=1200, y=500)

    D12 = Radiobutton(window, text="hexidecimal", value=2, variable=dec_cipher_type)
    D12.configure(background='#1C1C1C', activebackground='#1C1C1C', foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D12['font']= font.Font(family='Helvetica', size=11)
    D12.place(x=1300, y=500)

    D13 = Radiobutton(window, text="binary", value=3, variable=dec_cipher_type)
    D13.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D13['font']= font.Font(family='Helvetica', size=11)
    D13.place(x=1420, y=500)

    # --------- Key --------- #

    dec_key = StringVar()

    dec_keyLabel = Label(text='Enter Key:')
    dec_keyLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    dec_keyLabel.place(x=25, y=540)

    dec_keyBox = ttk.Entry(window, width=115,  font=50, textvariable=dec_key)
    dec_keyBox.place(x=225, y=540)

    dec_key_type = IntVar(None, 1)

    D21 = Radiobutton(window, text="plaintext", value=1, variable=dec_key_type)
    D21.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D21['font']= font.Font(family='Helvetica', size=11)
    D21.place(x=1200, y=570)

    D22 = Radiobutton(window, text="hexidecimal", value=2, variable=dec_key_type)
    D22.configure(background='#1C1C1C', activebackground='#1C1C1C', foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D22['font']= font.Font(family='Helvetica', size=11)
    D22.place(x=1300, y=570)

    D23 = Radiobutton(window, text="binary", value=3, variable=dec_key_type)
    D23.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D23['font']= font.Font(family='Helvetica', size=11)
    D23.place(x=1420, y=570)

    dec_key.trace("w", lambda *args: character_limit(dec_key, dec_key_type))


    # --------- IV --------- #

    dec_initVector = StringVar()

    dec_initVectorLabel = Label(text='Enter Initialization Vector:')
    dec_initVectorLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    dec_initVectorLabel.place(x=25, y=600)

    dec_initVectorBox = ttk.Entry(window, width=115, font=50, textvariable=dec_initVector)
    dec_initVectorBox.place(x=225, y=610)

    dec_initVector_type = IntVar(None, 1)

    D31 = Radiobutton(window, text="plaintext", value=1, variable=dec_initVector_type)
    D31.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D31['font']= font.Font(family='Helvetica', size=11)
    D31.place(x=1200, y=640)

    D32 = Radiobutton(window, text="hexidecimal", value=2, variable=dec_initVector_type)
    D32.configure(background='#1C1C1C', activebackground='#1C1C1C', foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D32['font']= font.Font(family='Helvetica', size=11)
    D32.place(x=1300, y=640)

    D33 = Radiobutton(window, text="binary", value=3, variable=dec_initVector_type)
    D33.configure(background='#1C1C1C', activebackground='#1C1C1C',  foreground='white', activeforeground='white', selectcolor='#1C1C1C')
    D33['font']= font.Font(family='Helvetica', size=11)
    D33.place(x=1420, y=640)

    dec_initVector.trace("w", lambda *args: character_limit(dec_initVector, dec_initVector_type))

    # --------- Result --------- #

    dec_messageLabel = Label(text='Resulting Message:')
    dec_messageLabel.configure(background='#1C1C1C', font=50, fg='white', justify='left', wraplengt=190)
    dec_messageLabel.place(x=25, y=680)

    dec_messageBox = Label()
    dec_messageBox.configure(background='#FFFFFF', width=115, height=1, font=50, fg='red', justify='left', wraplengt=1250)
    dec_messageBox.pack(anchor="w")
    dec_messageBox.place(x=225, y=680)

    # --------- Button --------- #

    dec_decryptionButton = ttk.Button(window,
                                  text='Decrypt',
                                  command=lambda: decrypt(dec_cipher, dec_cipher_type, dec_key, dec_key_type, dec_initVector, dec_initVector_type, dec_messageBox))
    dec_decryptionButton.place(x=725, y=730)

    # ----------------------------------------------------------------------- #

    window.mainloop()

main()