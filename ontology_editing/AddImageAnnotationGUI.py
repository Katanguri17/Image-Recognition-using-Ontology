from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from owlready2 import *
from functools import partial
import os

import OntoEditModule as OEM

cwd = os.path.dirname(os.path.realpath('__file__'))
par_dir=os.path.dirname(cwd)
data_dir=par_dir+'/data'


    
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
    display_img=ImageTk.PhotoImage(display_img.resize((400,int(h*400/w))))
    display_img_label.configure(image=display_img)
    display_img_label.photo=display_img
    submit_button.grid(row=3,column=0,columnspan=2,ipady=10,padx=5,pady=5)
    # display_img_label.grid(row=1,column=0,padx=5,pady=5,columnspan=3)

def show_add_menu():
    global isNewDancer
    isNewDancer=True
    select_dancer_frame.grid_remove()
    enter_dancer_frame.grid(row=4,column=0) 

def show_select_menu():
    global isNewDancer
    isNewDancer=False
    enter_dancer_frame.grid_remove()
    select_dancer_frame.grid(row=2,column=0)

def show_asam_menu():
    global isSamyukta
    isSamyukta=False
    select_sam_frame.grid_remove()
    select_asam_frame.grid(row=3,column=0,columnspan=2)

def show_sam_menu():
    global isSamyukta
    isSamyukta=True
    select_asam_frame.grid_remove()
    select_sam_frame.grid(row=5,column=0,columnspan=2)

def submit(clicked,gender_val,sam_val,lefthand_val,righthand_val):
    global image_path
    print(image_path)
    img_to_add=OEM.add_new_image_instance(image_path)
    if isNewDancer:
        print(str(Dancer_name_entry.get())+' '+Dancer_age_entry.get()+' '+gender_val.get())
        if gender_val.get()=='Male':
            _dancer_gender=0
        else:
            _dancer_gender=1
        dancer_in_img=OEM.add_new_dancer_instance(Dancer_name_entry.get(),int(Dancer_age_entry.get()),_dancer_gender)
    else:
        print(clicked.get())
        dancer_in_img=OEM.onto.search_one(hasDancerId=int(clicked.get().split('\t')[0].split(':')[1]))
        if update_name_entry.get() !='':
            dancer_in_img.update_dancer_info(_add_name=update_name_entry.get())
        print('Updated name: ',update_name_entry.get())
    

    if isSamyukta:
        print(sam_val.get())
        sam_id=int(sam_val.get().split('\t')[0].split(':')[1])
        img_static_desc=OEM.add_new_static_instance(_dance_name=Dance_name_entry.get(),_is_samyukta=isSamyukta,_samyukta=sam_id)
    else:   
        print(lefthand_val.get(),' ',righthand_val.get())
        l_id=int(lefthand_val.get().split('\t')[0].split(':')[1])
        r_id=int(righthand_val.get().split('\t')[0].split(':')[1])
        img_static_desc=OEM.add_new_static_instance(_dance_name=Dance_name_entry.get(),_is_samyukta=isSamyukta,_left=l_id,_right=r_id)

    OEM.add_new_content_instance(img_to_add,dancer_in_img,img_static_desc)


if __name__=='__main__':
    root = Tk()
    root.title("Dance Image Annotator")

    path_selector=Frame(root)
    path_selector.grid(row=0,column=0,columnspan=2)
    img_path_label=Label(path_selector,text='Image Path')
    img_path_label.grid(row=0, column=0,padx=10,pady=10)
    
    img_path_entry=Entry(path_selector,width=90)
    img_path_entry.grid(row=0,column=1,padx=10,pady=10,ipady=5)

    file_explore = Button(path_selector, text = "Browse...",command = partial(fileClick))
    file_explore.grid(column = 2, row = 0, padx="5", pady="5")
    
    image_frame=Frame(root,highlightthickness=2,highlightbackground='black')
    image_frame.grid(row=1,column=0)
    display_img_label=Label(image_frame)
    display_img=Image.open('gear.jpg')
    w,h=display_img.size
    display_img=ImageTk.PhotoImage(display_img.resize((400,int(h*400/w))))
    display_img_label.configure(image=display_img)
    display_img_label.photo=display_img
    display_img_label.grid(row=1,column=0,padx=5,pady=5,columnspan=3)
    
    dancer_frame=Frame(root,highlightthickness=2,highlightbackground='black')
    dancer_frame.grid(row=1,column=1,padx=10,pady=10)
    dancer_label=Label(dancer_frame,text='Dancer details')
    dancer_label.grid(row=0,column=0,padx=10,pady=10)
    isNewDancer=True
    select_button=Button(dancer_frame,text='Select a dancer from records',command=show_select_menu,width=70)
    select_dancer_frame=Frame(dancer_frame)

    enter_dancer_button=Button(dancer_frame,text='Add new dancer',command=show_add_menu,width=70)
    enter_dancer_frame=Frame(dancer_frame)
    Dancer_name_label = Label(enter_dancer_frame,text="Dancer Name")
    Dancer_name_label.grid(row=0,column=0,padx=5,pady=5)#,padx=10,pady=10,ipady=10)
    
    Dancer_name_entry = Entry(enter_dancer_frame,width=50)
    Dancer_name_entry.grid(row=0,column=1,padx=5,pady=5,ipady=5)#,padx=10,pady=10,ipady=5)
    
    Dancer_age_label = Label(enter_dancer_frame,text="Dancer Age")
    Dancer_age_label.grid(row=1,column=0,padx=5,pady=5)#,padx=10,pady=10)
    
    Dancer_age_entry = Entry(enter_dancer_frame,width=50)
    Dancer_age_entry.grid(row=1,column=1,padx=5,pady=5,ipady=5)#,padx=10,pady=10,ipady=5)
    
    Dancer_gender_label=Label(enter_dancer_frame,text="Dancer Gender")
    Dancer_gender_label.grid(row=2,column=0,padx=5,pady=5)
    gender=['Male', 'Female']
    gender_val=StringVar(enter_dancer_frame)
    gender_val.set("--Select--")
    
    Dancer_gender = OptionMenu(enter_dancer_frame,gender_val,*gender)
    Dancer_gender.configure(width=10,height=2)
    Dancer_gender.grid(row=2,column=1,padx=5,pady=5)#,padx=10,pady=10)

    select_dancer_frame=Frame(dancer_frame)
    dancer_options = ['ID:'+str(dancer.hasDancerId)+'\tNames:'+str(dancer.hasDancerName)+'\tAge:'+str(dancer.hasDancerAge)+'\tGenger:'+dancer.hasDancerGender for dancer in OEM.onto.Dancer.instances()]
    clicked=StringVar()
    clicked.set('--Select--')
    
    select_dancer_label=Label(select_dancer_frame,text='Select dancer')
    select_dancer_label.grid(row=0,column=0,padx=5,pady=5)
    dancer_dropdown = OptionMenu(select_dancer_frame,clicked,*dancer_options)
    dancer_dropdown.configure(width=55,height=2)
    dancer_dropdown.grid(column = 1,row = 0,padx=5,pady=5)#, padx="5", pady="5"
    update_name_label = Label(select_dancer_frame,text="Add/Update\nDancer Name")
    update_name_label.grid(row=1,column=0,padx=5,pady=5)#,padx=10,pady=10,ipady=10)
    
    update_name_entry = Entry(select_dancer_frame,width=50)
    update_name_entry.grid(row=1,column=1,padx=5,pady=5,ipady=5)

    select_button.grid(row=1,column=0,ipady=10)
    enter_dancer_button.grid(row=3,column=0,ipady=10)


    hastamudra_frame=Frame(root,highlightthickness=2,highlightbackground='black')
    hastamudra_frame.grid(row=2,column=0,columnspan=2,padx=10,pady=10)
    hastamudra_label=Label(hastamudra_frame,text='Dance details')
    hastamudra_label.grid(row=0,column=0,padx=10,pady=10,columnspan=2)
    isSamyukta=True
    dance_name_label=Label(hastamudra_frame,text='Dance name')
    dance_name_label.grid(row=1,column=0,padx=10,pady=10)
    Dance_name_entry = Entry(hastamudra_frame,width=50)
    Dance_name_entry.grid(row=1,column=1,padx=5,pady=5,ipady=5)#,padx=10,pady=10,ipady=5)

    asam_button=Button(hastamudra_frame,text='Asamyukta Mudra',command=show_asam_menu,width=70)
    select_asam_frame=Frame(hastamudra_frame)

    sam_button=Button(hastamudra_frame,text='Samyukta Mudra',command=show_sam_menu,width=70)
    select_sam_frame=Frame(hastamudra_frame)

    asam_options=['ID:'+str(mudra.hasMudraId)+'\t'+str(mudra.name).split('_')[0] for mudra in OEM.onto.AsamyuktaMudra.instances()]
    
    lefthand_label = Label(select_asam_frame,text="Select left-\nhand Mudra")
    lefthand_label.grid(row=0,column=0,padx=5,pady=5)#,padx=10,pady=10,ipady=10)
    
    lefthand_val=StringVar(select_asam_frame)
    lefthand_val.set('--Select--')

    righthand_label = Label(select_asam_frame,text="Select right-\nhand Mudra")
    righthand_label.grid(row=1,column=0,padx=5,pady=5)#,padx=10,pady=10,ipady=10)

    righthand_val=StringVar(select_asam_frame)
    righthand_val.set('--Select--')
    
    lefthand_menu = OptionMenu(select_asam_frame,lefthand_val,*asam_options)
    lefthand_menu.grid(row=0,column=1,padx=5,pady=5)#,padx=10,pady=10)
    lefthand_menu.configure(width=55,height=2)

    righthand_menu = OptionMenu(select_asam_frame,righthand_val,*asam_options)
    righthand_menu.grid(row=1,column=1,padx=5,pady=5)#,padx=10,pady=10)
    righthand_menu.configure(width=55,height=2)
    
    sam_options=['ID:'+str(mudra.hasMudraId)+'\t'+str(mudra.name).split('_')[0] for mudra in OEM.onto.SamyuktaMudra.instances()]
    sam_label=Label(select_sam_frame,text='Select samyukta\nmudra')
    sam_label.grid(row=0,column=0,padx=5,pady=5)
    sam_val=StringVar(select_sam_frame)
    sam_val.set('--Select--')
    sam_dropdown = OptionMenu(select_sam_frame,sam_val,*sam_options)
    sam_dropdown.configure(width=55,height=2)
    sam_dropdown.grid(column = 1,row = 0,padx=5,pady=5)#, padx="5", pady="5"
    

    asam_button.grid(row=2,column=0,columnspan=2,ipady=10)
    sam_button.grid(row=4,column=0,columnspan=2,ipady=10) 

    submit_button = Button(root, text='Submit', command=partial(submit,clicked,gender_val,sam_val,lefthand_val,righthand_val))
    
    root.mainloop()
    

