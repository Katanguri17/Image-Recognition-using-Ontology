from re import L
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from owlready2 import *
from functools import partial
import os

import OntoEditModule as OEM
import OntoQueryModule as OQM


if __name__ == '__main__':
    root = Tk()
    root.title('Query Window')
    #query_frame = Frame(root)
    # query_the_onto = Button(root, text='Query the database',
    #                         command=partial(query), width=80)
    # query_the_onto.grid(row=4, column=0)
    Dancer_name_label=Label(root, text='Dancer Name')
    Dancer_name_label.grid(row=0,column=0,rowspan=2)
    
    Dancer_name_entry = Entry(root,width=80)
    Dancer_name_entry.grid(row=1,column=0)
    
    Dancer_id_label = Label(root,text='Dancer ID')
    Dancer_id_label.grid(row=3,column=0,rowspan=2)
    
    Dancer_id_entry = Entry(root,width=80)
    Dancer_id_entry.grid(row=4,column=0)
    
    Dancer_age_label = Label(root,width=80)
    Dancer_age_label.grid(row=5,column=0)
    
    Dancer_age_entry = Entry(root,width=80)
    Dancer_age_entry.grid(row=6,column=0)
    
    Dancer_gender_label = Label(root,text='Gender')
    Dancer_gender_label.grid(row=7,column=0)
    
    Dancer_gender_entry = Entry(root,width=80)
    Dancer_gender_entry.grid(row=8,column=0)
    
    Dancer_name_label = Label(root,text='Dancer name')
    Dancer_name_label.grid(row=9,column=0)
    
    Dance_name_entry = Entry(root,width=80)
    Dancer_name_entry.grid(row=10,column=0)
    
    Sam_mudra_label = Label(root,text='Sam Mudra')
    Sam_mudra_label.grid(row=11,column=0)
    
    Sam_mudra_entry = Entry(root,width=80)
    Sam_mudra_entry.grid(row=12,column=0)
    
    L_mudra_label= Label(root,text='Left hand Mudra')
    L_mudra_label.grid(row=13,column=0)
    
    L_mudra_entry= Entry(root,width=80)
    L_mudra_entry.grid(row=14,column=0)
    
    R_mudra_label= Label(root,text='Right hand Mudra')
    R_mudra_label.grid(row=15,column=0)
    
    R_mudra_entry = Entry(root,width=80)
    R_mudra_entry.grid(row=16,column=0)
    
    Dict={'dancer_name':Dancer_name_entry.get(),'dancer_age':Dancer_age_entry.get(),'dancer_gender':Dancer_gender_entry.get(),'dance_name':Dance_name_entry.get(),'sam_mudra':Sam_mudra_entry.get(),'l_mudra':L_mudra_entry.get(),'r_mudra':R_mudra_entry.get()}
    
    submit_button= Button(root,text='Submit',command=partial(OQM.generate_query(Dict)))
    submit_button= Button.grid(row=17,column=0)
    
    
    root.mainloop()
