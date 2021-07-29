#GUI Implementation
import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import stegan as st
from tkinter import messagebox as mb


class Steganogram:


    def enc(self):
        print("IN :: ENC")
        inputImgPath = pathImgEnc.get("1.0", 'end-1c')  #end-1c to ignore insertion of \n
        inputTxtPath = pathTxtEnc.get("1.0", 'end-1c')

        if inputImgPath != "" and inputTxtPath != "":
            image = Image.open(inputImgPath, 'r')
            f = open(inputTxtPath, "r")
            data = f.read()
            print(type(data))
            print("File Data :: ", data)
            new_img = image.copy()
            st.encode_enc(new_img, data)
            st.decode_dec(new_img)
            p_img = ImageTk.PhotoImage(new_img)

            e_width = p_img.width()
            e_height = p_img.height()
            print("old width :: height ::: "+str(e_width)+" :: "+str(e_height))

            e_width, e_height = self.transform(p_img.width(), p_img.height())

            """
            if e_width > 500 or e_height > 500:
                while e_width>450 or e_height > 450:
                    e_width = e_width / 2
                    e_height = e_height / 2
            """
            print("new width :: height ::: "+str(e_width)+" :: "+str(e_height))

            n_img = ImageTk.PhotoImage(new_img.resize((int(e_width), int(e_height)), Image.ANTIALIAS))

            #Reconfig Surface with decrypted image
            canvas_Img.configure(width=e_width, height=e_height, image=n_img)
            canvas_Img.width = e_width
            canvas_Img.height = e_height
            canvas_Img.image = n_img

            #Save File
            simgenc = fd.asksaveasfilename(initialdir="/", title="Select file", defaultextension='.png', filetypes=(("png files", "*.png"), ("all files", "*.*")))
            print(simgenc)
            if simgenc:
                new_img.save(simgenc, str(simgenc.split(".")[1].upper()))
                mb.showinfo(title=windowTitle, message=str("File Saved Successfully as "+simgenc))
            else:
                mb.showwarning(title=windowTitle, message="Operation Cancelled..!!!")
        else:
            mb.showerror(title=windowTitle, message="Empty Input...!!")



    def dec(self):
        inputImgPathD = pathImgDec.get("1.0", 'end-1c')

        decoded_str = ""
        if inputImgPathD != "":
            imageD = Image.open(inputImgPathD, 'r')
            decoded_str = st.decode_dec(imageD)
            d_txt.delete(1.0, tk.END)
            d_txt.insert(1.0, str(decoded_str))

            stxtenc = fd.asksaveasfilename(initialdir="/", title="Select file", defaultextension='.txt', filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            if stxtenc:
                f = open(stxtenc, "w")
                print("Writing to File...")
                f.write(decoded_str)
                f.close()
                mb.showinfo(title=windowTitle,message=str("File Saved Successfully as "+stxtenc))
            else:
                mb.showwarning(title=windowTitle, message="Operation Cancelled..!!!")
        else:
            mb.showerror(title=windowTitle, message="Empty Input...!!")




    def getImgEnc(self):
        imgnameenc = fd.askopenfilename(initialdir="/", title="Select Cover Image file to Encrypt", filetypes=(("jpeg files", "*.jpg"), ("PNG files", "*.png"), ("all files", "*.*")))
        print(imgnameenc)
        pathImgEnc.delete(1.0, tk.END)
        pathImgEnc.insert(1.0, imgnameenc)


    def getTxtEnc(self):
        txtnameenc = fd.askopenfilename(initialdir="/", title="Select Text file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        print(txtnameenc)
        pathTxtEnc.delete(1.0, tk.END)
        pathTxtEnc.insert(1.0, txtnameenc)

    def getImgDec(self):
        imgnamedec = fd.askopenfilename(initialdir="/", title="Select Image file to Decrypt", filetypes=(("PNG files", "*.png"), ("all files", "*.*")))
        print(imgnamedec)
        pathImgDec.delete(1.0, tk.END)
        pathImgDec.insert(1.0, imgnamedec)


    def transform(self, w, h):
        wn = 0
        hn = 0
        if w >= h:
            if w > 450:
                wn = 450
                hn = h/(w/wn)
            else:
                wn = w
                hn = h
                """
            elif w < 450 and ( w != 1 or w != 0):
                wn = 450
                hn = h * (wn/w)
                """
        elif h >= w:
            if h > 450:
                hn = 450
                wn = w/(h/hn)
            else:
                hn = h
                wn = w
                """
            elif h < 450 and (h != 1 or h != 0):
                hn = 450
                wn = w * (hn/h)
                """
        return wn, hn


if __name__ == '__main__':

    obj = Steganogram()

    #Configure root window
    root = tk.Tk()
    root.resizable(False, False)
    windowTitle = "Steganogram"
    root.title(windowTitle)

    """Top Pane :: Radio Buttons"""
    paneTop = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    paneTop.grid(column=0, row=0, columnspan=2)

    radioEnc = tk.Label(paneTop, text="Encryption", background="darkgrey")
    paneTop.add(radioEnc)

    radioDec = tk.Label(paneTop, text="Decryption")
    paneTop.add(radioDec)


    """ Bottom Pane"""
    paneBottom = tk.PanedWindow(root, background="Black", width=1000, height=610)
    paneBottom.grid(column=0, row=1, columnspan=2)


    """ Left Bottom Frame """
    frameLeft = tk.Frame(paneBottom, background="darkgrey", width=600)
    paneBottom.add(frameLeft)
    paneBottom.paneconfig(frameLeft, minsize=500)

    lblSelImgEnc = tk.Label(frameLeft, text="Select Cover Image : ")
    lblSelImgEnc.grid(column=0, row=1, columnspan=1, sticky=tk.NW)
    pathImgEnc = tk.Text(frameLeft, height=1, width=40)
    pathImgEnc.grid(column=1, row=1, columnspan=1, sticky=tk.N)
    btnSelImgEnc = tk.Button(frameLeft, text="Browse", command=obj.getImgEnc)
    btnSelImgEnc.grid(column=2, row=1, columnspan=1, sticky=tk.E)

    lblSelTxtEnc = tk.Label(frameLeft, text="Select Text to Encrypt : ")
    lblSelTxtEnc.grid(column=0, row=2, columnspan=1, sticky=tk.W)
    pathTxtEnc = tk.Text(frameLeft, height=1, width=40)
    pathTxtEnc.grid(column=1, row=2, columnspan=1)
    btnSelTxtEnc = tk.Button(frameLeft, text="Browse", command=obj.getTxtEnc)
    btnSelTxtEnc.grid(column=2, row=2, columnspan=1, sticky=tk.E)

    btnEnc = tk.Button(frameLeft, text="Encrypt", command=obj.enc)
    btnEnc.grid(column=0, row=3, columnspan=3, sticky=tk.N)

    frameEnc = tk.LabelFrame(frameLeft, text="Output", height=500, width=500)
    frameEnc.grid(column=0, row=4, columnspan=3, sticky=tk.N)
    mimg=ImageTk.PhotoImage(file="alpha.png")

    canvas_Img = tk.Label(frameEnc,image=mimg,width=470,height=470)
    canvas_Img.grid(column=1,row=4,columnspan=3,sticky=tk.NSEW)

    #btnSaveEnc = tk.Button(frameLeft, text="Save Output", command=saveImgEnc)
    #btnSaveEnc.grid(column=0, row=5, columnspan=3, sticky=tk.S)


    """ Right Bottom Frame """
    frameRight = tk.Frame(paneBottom, background="lightgrey", width=600)

    paneBottom.add(frameRight)
    paneBottom.paneconfig(frameRight, minsize=500)

    lblselImgDec = tk.Label(frameRight, text="Image to Decrypt : ")
    lblselImgDec.grid(column=0, row=1, columnspan=1, sticky=tk.NW)
    pathImgDec = tk.Text(frameRight, height=1, width=40)
    pathImgDec.grid(column=1, row=1, columnspan=1, sticky=tk.N)
    btnSelImgDec = tk.Button(frameRight, text="Browse", command=obj.getImgDec)
    btnSelImgDec.grid(column=2, row=1, columnspan=1, sticky=tk.E)

    btnDec = tk.Button(frameRight, text="Decrypt", command=obj.dec)
    btnDec.grid(column=1, row=2, pady=13, sticky=tk.S)

    frameDec = tk.LabelFrame(frameRight, text="Output", height=495, width=500)
    frameDec.grid(column=0, row=3, columnspan=3, sticky=tk.N)

    d_txt = tk.Text(frameRight, width=55, height=29)
    d_txt.insert(tk.END, "Decrypted Content Will Be Displayed Here...")
    d_txt.grid(column=0, row=3, columnspan=3, pady=2, sticky=tk.S)

    #btnSaveDec = tk.Button(frameRight, text="Save Output", command=saveTxtDec)
    #btnSaveDec.grid(column=0, row=4, columnspan=3, sticky=tk.S)
    root.mainloop()
