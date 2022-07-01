from re import L
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from owlready2 import *
from functools import partial
import os

import OntoEditModule as OEM
import OntoQueryModule as OQM


def show_asam_menu():
    global isSamyukta
    isSamyukta = False
    select_sam_frame.grid_remove()
    select_asam_frame.grid(row=3, column=0, columnspan=2)


def show_sam_menu():
    global isSamyukta
    isSamyukta = True
    select_asam_frame.grid_remove()
    select_sam_frame.grid(row=5, column=0, columnspan=2)


def submit_function(gender_val, sam_val, lefthand_val, righthand_val):

    query={}
    print(Dancer_name_entry.get())
    if Dancer_name_entry.get()!='':
        query['dancer_name']=Dancer_name_entry.get()
    else:
        query['dancer_name']=None

    if Dancer_id_entry.get()!='':
        query['dancer_id']=Dancer_id_entry.get()
    else:
        query['dancer_id']=None

    if Dancer_age_entry.get()!='':
        query['dancer_age']=Dancer_age_entry.get()
    else:
        query['dancer_age']=None

    if gender_val.get()!='--Select--':
        query['dancer_gender']=gender_val.get()[:1]
    else:
        query['dancer_gender']=None

    if Dance_name_entry.get()!='':
        query['dance_name']=Dance_name_entry.get()
    else:
        query['dance_name']=None

    if isSamyukta:
        if sam_val.get()!='--Select--':
            query['sam_mudra']=int(sam_val.get().split('\t')[0].split(':')[1])
        else:
            query['sam_mudra']=None
        query['l_mudra']=None
        query['r_mudra']=None

    else:
        query['sam_mudra']=None
        if lefthand_val.get()!='--Select--':
            query['l_mudra']=int(lefthand_val.get().split('\t')[0].split(':')[1])
        else:
            query['l_mudra']=None
        if righthand_val.get()!='--Select--':
            query['r_mudra']=int(righthand_val.get().split('\t')[0].split(':')[1])
        else:
            query['r_mudra']=None
        
    print(query)

    #print(query)
    Query = OQM.generate_query(query)
    #print(Query)
    L = list(default_world.sparql(Query))

    newWindow = Toplevel(root)
    newWindow.title("Results")

    i = 1

    for path in L:
        print(path[0])
        display_img_label = Label(newWindow)
        
        display_img = Image.open(path[0])
        w, h = display_img.size
        display_img = ImageTk.PhotoImage(display_img.resize((400, int(h*400/w))))
        display_img_label.configure(image=display_img)
        display_img_label.photo = display_img
        if(i % 2):
            Label_path = Label(newWindow, text=path[0], fg='red',width=40,height=5,wraplength=400)
        else:
            Label_path = Label(newWindow, text=path[0], fg='blue',width=40,height=5,wraplength=400)
        Label_path.pack()
        display_img_label.pack()
        i += 1



if __name__ == '__main__':
    root = Tk()
    root.title('Query Window')
    root.minsize(400, 400)
    # root.geometry("250*250")
    #query_frame = Frame(root)
    # query_the_onto = Button(root, text='Query the database',
    #                         command=partial(query), width=80)
    # query_the_onto.grid(row=4, column=0)
    Dancer_name_label = Label(root, text='Dancer Name')
    Dancer_name_label.grid(row=0, column=0)

    Dancer_name_entry = Entry(root, width=60)
    Dancer_name_entry.grid(row=0, column=1,padx=5,pady=5,ipady=5)

    Dancer_id_label = Label(root, text='Dancer ID')
    Dancer_id_label.grid(row=2, column=0)

    Dancer_id_entry = Entry(root, width=60)
    Dancer_id_entry.grid(row=2, column=1,padx=5,pady=5,ipady=5)

    Dancer_age_label = Label(root, text='Dancer Age')
    Dancer_age_label.grid(row=3, column=0)

    Dancer_age_entry = Entry(root, width=60)
    Dancer_age_entry.grid(row=3, column=1,padx=5,pady=5,ipady=5)

    Dancer_gender_label = Label(root, text='Gender')
    Dancer_gender_label.grid(row=4, column=0)

    gender = ['--Select--','Male', 'Female']
    gender_val = StringVar(root)
    gender_val.set(gender[0])

    Dancer_gender = OptionMenu(root, gender_val, *gender)
    Dancer_gender.configure(width=10, height=2)
    Dancer_gender.grid(row=4, column=1, padx=5, pady=5)

    hastamudra_frame = Frame(root)
    hastamudra_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    # hastamudra_label = Label(hastamudra_frame, text='Dance details')
    # hastamudra_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    isSamyukta = True
    dance_name_label = Label(hastamudra_frame, text='Dance name')
    dance_name_label.grid(row=1, column=0, padx=10, pady=10)
    Dance_name_entry = Entry(hastamudra_frame, width=60)
    # ,padx=10,pady=10,ipady=5)
    Dance_name_entry.grid(row=1, column=1, padx=5, pady=5, ipady=5)

    asam_button = Button(
        hastamudra_frame, text='Asamyukta Mudra', command=show_asam_menu, width=70)
    select_asam_frame = Frame(hastamudra_frame)

    sam_button = Button(hastamudra_frame, text='Samyukta Mudra',
                        command=show_sam_menu, width=70)
    select_sam_frame = Frame(hastamudra_frame)

    asam_options=['--Select--']
    asam_options.extend(['ID:'+str(mudra.hasMudraId)+'\t'+str(mudra.name).split('_')[0]
                    for mudra in OEM.onto.AsamyuktaMudra.instances()])

    lefthand_label = Label(select_asam_frame, text="Select left-\nhand Mudra")
    # ,padx=10,pady=10,ipady=10)
    lefthand_label.grid(row=0, column=0, padx=5, pady=5)

    lefthand_val = StringVar(select_asam_frame)
    lefthand_val.set('--Select--')

    righthand_label = Label(
        select_asam_frame, text="Select right-\nhand Mudra")
    # ,padx=10,pady=10,ipady=10)
    righthand_label.grid(row=1, column=0, padx=5, pady=5)

    righthand_val = StringVar(select_asam_frame)
    righthand_val.set('--Select--')

    lefthand_menu = OptionMenu(select_asam_frame, lefthand_val, *asam_options)
    lefthand_menu.grid(row=0, column=1, padx=5, pady=5)  # ,padx=10,pady=10)
    lefthand_menu.configure(width=55, height=2)

    righthand_menu = OptionMenu(
        select_asam_frame, righthand_val, *asam_options)
    righthand_menu.grid(row=1, column=1, padx=5, pady=5)  # ,padx=10,pady=10)
    righthand_menu.configure(width=55, height=2)

    sam_options=['--Select--']
    sam_options.extend(['ID:'+str(mudra.hasMudraId)+'\t'+str(mudra.name).split('_')[0]
                   for mudra in OEM.onto.SamyuktaMudra.instances()])
    sam_label = Label(select_sam_frame, text='Select samyukta\nmudra')
    sam_label.grid(row=0, column=0, padx=5, pady=5)
    sam_val = StringVar(select_sam_frame)
    sam_val.set('--Select--')
    sam_dropdown = OptionMenu(select_sam_frame, sam_val, *sam_options)
    sam_dropdown.configure(width=55, height=2)
    sam_dropdown.grid(column=1, row=0, padx=5, pady=5)  # , padx="5", pady="5"

    asam_button.grid(row=2, column=0, columnspan=2, ipady=10)
    sam_button.grid(row=4, column=0, columnspan=2, ipady=10)

    #print(Dancer_gender_entry.get())
    
    submit_button = Button(root, text='Submit',command=partial(submit_function,gender_val, sam_val, lefthand_val, righthand_val))
    submit_button.grid(row=6, column=0,columnspan=2,padx=5,pady=5,ipady=10)

    root.mainloop()
