from re import L
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from owlready2 import *
from functools import partial
import os

import OntoEditModule as OEM
import OntoQueryModule as OQM


def submit_function():

    query = {'dancer_name': Dancer_name_entry.get(), 'dancer_age': Dancer_age_entry.get(), 'dancer_gender': Dancer_gender_entry.get(
    ), 'dance_name': Dance_name_entry.get(), 'sam_mudra': Sam_mudra_entry.get(), 'l_mudra': L_mudra_entry.get(), 'r_mudra': R_mudra_entry.get()}

    #print(query)
    
    if(query['dancer_name'] == ""):
        query['dancer_name'] = None

    if(query['dancer_age'] == ""):
        query['dancer_age'] = None

    if(query['dancer_gender'] == ""):
        query['dancer_gender'] = None

    if(query['dance_name'] == ""):
        query['dance_name'] = None

    if(query['sam_mudra'] == ""):
        query['sam_mudra'] = None

    if(query['l_mudra'] == ""):
        query["l_mudra"] = None

    if(query["r_mudra"] == ""):
        query["r_mudra"] = None
        
    
    #print(query)
    Query = OQM.generate_query(query)
    #print(Query)
    L = list(default_world.sparql(Query))

    newWindow = Toplevel(root)
    newWindow.title("Results")

    i = 1

    for path in L:
        if(i % 2):
            Label_path = Label(newWindow, text=path, fg='red')
        else:
            Label_path = Label(newWindow, text=path, fg='blue')
        Label_path.grid(row=i, column=0)
        i += 1

    # print(L)


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

    Dancer_name_entry = Entry(root, width=80)
    Dancer_name_entry.grid(row=1, column=0)

    Dancer_id_label = Label(root, text='Dancer ID')
    Dancer_id_label.grid(row=2, column=0)

    Dancer_id_entry = Entry(root, width=80)
    Dancer_id_entry.grid(row=3, column=0)

    Dancer_age_label = Label(root, text='Dancer Age')
    Dancer_age_label.grid(row=4, column=0)

    Dancer_age_entry = Entry(root, width=80)
    Dancer_age_entry.grid(row=5, column=0)

    Dancer_gender_label = Label(root, text='Gender')
    Dancer_gender_label.grid(row=6, column=0)

    Dancer_gender_entry = Entry(root, width=80)
    Dancer_gender_entry.grid(row=7, column=0)

    Dance_name_label = Label(root, text='Dance name')
    Dance_name_label.grid(row=8, column=0)

    Dance_name_entry = Entry(root, width=80)
    Dance_name_entry.grid(row=9, column=0)

    Sam_mudra_label = Label(root, text='Sam Mudra')
    Sam_mudra_label.grid(row=10, column=0)

    Sam_mudra_entry = Entry(root, width=80)
    Sam_mudra_entry.grid(row=11, column=0)

    L_mudra_label = Label(root, text='Left hand Mudra')
    L_mudra_label.grid(row=12, column=0)

    L_mudra_entry = Entry(root, width=80)
    L_mudra_entry.grid(row=13, column=0)

    R_mudra_label = Label(root, text='Right hand Mudra')
    R_mudra_label.grid(row=14, column=0)

    R_mudra_entry = Entry(root, width=80)
    R_mudra_entry.grid(row=15, column=0)

    #print(Dancer_gender_entry.get())
    
    submit_button = Button(root, text='Submit',
                           command=submit_function)
    submit_button.grid(row=16, column=0)

    root.mainloop()
