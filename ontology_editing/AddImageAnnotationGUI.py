from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial
import os

import OntoEditModule as OEM

cwd = os.path.dirname(os.path.realpath(__file__))
par_dir=os.path.dirname(cwd)
data_dir=par_dir+r'/data/'

def fileClick():
    global image_path
    image_path = filedialog.askopenfilename(initialdir = data_dir, title = "Select a File", filetypes = (("jpg files","*.jpg*"),("JGP files","*.JPG*"),("png files","*.png*"),("PNG files","*.PNG*"),("All files","*.*")))
    img_path_entry.delete(0,END)
    if not image_path:
        img_path_entry.insert(0,"No file selected")
        return
    img_path_entry.insert(0,image_path)
    display_img=Image.open(image_path)
    w,h=display_img.size
    display_img=ImageTk.PhotoImage(display_img.resize((800,int(h*800/w))))
    display_img_label.configure(image=display_img)
    display_img_label.photo=display_img
    display_img_label.grid(row=1,column=0,padx=5,pady=5,columnspan=3)



if __name__=='__main__':
    root = Tk()
    root.title("Dance Image Annotator")
    
    dancer_options = [[dancer.hasDancerId,dancer.hasDancerName,dancer.hasDancerAge,dancer.hasDancerGender] for dancer in OEM.onto.Dancer.instances()]
    clicked=dancer_options[0]
    
    img_path_label=Label(root,text='Image Path')
    img_path_label.grid(row=0, column=0,padx=10,pady=10)
    
    img_path_entry=Entry(root,width=100)
    img_path_entry.grid(row=0,column=1,padx=10,pady=10,ipady=5)
    
    display_img_label=Label(root)
    
    file_explore = Button(root, text = "Browse...",command = partial(fileClick))
    file_explore.grid(column = 2, row = 0, padx="5", pady="5")
    
    dancer_info_label=Label(root,text='Dancer details')
    dancer_info_label.grid(row=2, column=0,padx=10,pady=10,columnspan=3)
    
    dancer_dropdown = OptionMenu(root,clicked,*dancer_options)
    dancer_dropdown.grid(column = 0,row = 3, padx="5", pady="5")
    
    root.mainloop()
    


