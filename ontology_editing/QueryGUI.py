from tkinter import *
from PIL import ImageTk, Image
from owlready2 import *
from functools import partial
from tkinter import ttk
import os
import pickle


import OntoEditModule as OEM
import OntoQueryModule as OQM
import Pre_process as PP

cwd = os.path.dirname(os.path.realpath('__file__'))
NLP_dir=os.path.dirname(cwd)+r'/NLP'

def add_to_unlearnt_dataset(text):
    text,l=PP.process(text)
    entities={'entities': []}
    print('Your query:',text)
    print('Annotate the keywords: ')
    print('- 0 if NA')
    print('- 1 if PERSON')
    print('- 2 if GENDER')
    print('- 3 if MUDRA')
    print('- 4 if FAC')

    for item in l:
        i=int(input('+ '+str(item)+': '))
        if i==0:
            continue
        elif i==1:
            entities['entities'].append((item[0],item[1],'PERSON'))
        elif i==2:
            entities['entities'].append((item[0],item[1],'GENDER'))
        elif i==3:
            entities['entities'].append((item[0],item[1],'MUDRA'))
        elif i==4:
            entities['entities'].append((item[0],item[1],'FAC'))

    print('Adding data sample:',(text,entities))
    f=open(NLP_dir+r'/unlearnt_bin','rb')
    train=pickle.load(f)
    f.close()

    train+=(text,entities)
    f=open(NLP_dir+r'/unlearnt_bin','wb')
    pickle.dump(train,f)
    f.close()

    f=open(NLP_dir+r'/.unlearnt_samples_cnt.txt','r')
    new_sample_cnt=int(f.read())+1
    f.close()

    f=open(NLP_dir+r'/.unlearnt_samples_cnt.txt','w')
    f.write(str(new_sample_cnt))
    f.close()



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

def show_open_query():
    global isOpen
    isOpen=True
    tight_query.grid_remove()
    open_query.grid(row=1,column=0)

def show_tight_query():
    global isOpen
    isOpen=False
    open_query.grid_remove()
    tight_query.grid(row=3,column=0)

def submit_function(gender_val, sam_val, lefthand_val, righthand_val):

    if isOpen:
        print('Performing an open query ...')
        asam_query,sam_query=OQM.generate_open_query(free_form_entry.get())
        L=[]
        if asam_query is not None:	
            print('Asamyukta mudra specific SPARQL query:',end='')
            print(asam_query,end='')
            l1=list(default_world.sparql(asam_query))
            print('Results:',[ s[0][-7:] for s in l1] )
            L=L+l1
        if sam_query is not None:
            print('Samyukta mudra specific SPARQL query:',end='')
            print(sam_query,end='')
            l2=list(default_world.sparql(sam_query))
            print('Results:',[ s[0][-7:] for s in l2])
            L=L+l2
    else:
        print('Performing a tight query ...')
        query={}
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
            
        print('Requirements dict.:',query)

        Query = OQM.generate_tight_query(query)
        print('SPARQL query:',Query,end='')
        L = list(default_world.sparql(Query))
        print('Results:',[s[0][-7:] for s in L])

    newWindow = Toplevel(root)
    newWindow.geometry("540x800")
    newWindow.title("Result")
    
    main_frame = Frame(newWindow)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    # Configure The Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    i = 1

    for path in L:
        #print(path[0])
        display_img_label = Label(second_frame)
        
        display_img = Image.open(path[0])
        w, h = display_img.size
        display_img = ImageTk.PhotoImage(display_img.resize((500, int(h*500/w))))
        display_img_label.configure(image=display_img)
        display_img_label.photo = display_img
        if(i % 2):
            Label_path = Label(second_frame, text=path[0], fg='red',width=40,height=5,wraplength=450)
        else:
            Label_path = Label(second_frame, text=path[0], fg='blue',width=40,height=5,wraplength=450)
        Label_path.pack()
        display_img_label.pack(padx=10)
        i += 1

    if isOpen:
        response=input('Will you help us by annotating your free-form query, this will help us give better results next time ?(y/n): ')
        if response.lower()=='y':
            add_to_unlearnt_dataset(free_form_entry.get())



if __name__ == '__main__':
    root=Tk()

    root.title('Query Window')
    # root.minsize(400, 400)

    isOpen=True
    open_query_button=Button(root, text='Make free form query', command=show_open_query, width=70)
    tight_query_button=Button(root, text='Make a tight query',command=show_tight_query,width=70)

    open_query_button.grid(row=0,column=0,padx=5,pady=5,ipady=10)
    tight_query_button.grid(row=2,column=0,padx=5,pady=5,ipady=10)

    open_query = Frame(root)
    tight_query = Frame(root)

    type_query_label=Label(open_query, text='Type you\nquery')
    type_query_label.grid(row=0,column=0)
    free_form_entry=Entry(open_query,width=60)
    free_form_entry.grid(row=0,column=1,padx=5,pady=5,ipady=5)
    
    # tight_query.geometry("250*250")
    #query_frame = Frame(tight_query)
    # query_the_onto = Button(tight_query, text='Query the database',
    #                         command=partial(query), width=80)
    # query_the_onto.grid(row=4, column=0)
    Dancer_name_label = Label(tight_query, text='Dancer Name')
    Dancer_name_label.grid(row=0, column=0)

    Dancer_name_entry = Entry(tight_query, width=60)
    Dancer_name_entry.grid(row=0, column=1,padx=5,pady=5,ipady=5)

    Dancer_id_label = Label(tight_query, text='Dancer ID')
    Dancer_id_label.grid(row=2, column=0)

    Dancer_id_entry = Entry(tight_query, width=60)
    Dancer_id_entry.grid(row=2, column=1,padx=5,pady=5,ipady=5)

    Dancer_age_label = Label(tight_query, text='Dancer Age')
    Dancer_age_label.grid(row=3, column=0)

    Dancer_age_entry = Entry(tight_query, width=60)
    Dancer_age_entry.grid(row=3, column=1,padx=5,pady=5,ipady=5)

    Dancer_gender_label = Label(tight_query, text='Gender')
    Dancer_gender_label.grid(row=4, column=0)

    gender = ['--Select--','Male', 'Female']
    gender_val = StringVar(tight_query)
    gender_val.set(gender[0])

    Dancer_gender = OptionMenu(tight_query, gender_val, *gender)
    Dancer_gender.configure(width=10, height=2)
    Dancer_gender.grid(row=4, column=1, padx=5, pady=5)

    hastamudra_frame = Frame(tight_query)
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
    submit_button.grid(row=4, column=0,padx=5,pady=5,ipady=10)

    root.mainloop()
