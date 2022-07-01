from owlready2 import *
import pandas as pd
import os
import PIL.Image

cwd = os.path.dirname(os.path.realpath('__file__'))
onto_filepath=cwd+r'/dance_dummy.owl'
onto = get_ontology('file://'+onto_filepath).load()

with onto:
    class Dancer(Thing):
        @classmethod
        def print_instances(cls):
            print('ID\tName\tAge\tGender')
            for dancer in Dancer.instances():
                print(str(dancer.hasDancerId)+'\t'+str(dancer.hasDancerName)+'\t'+str(dancer.hasDancerAge)+'\t'+dancer.hasDancerGender)
        
        def update_dancer_info(self, _add_name=None, _update_age=None):
            if _add_name is not None:
                self.hasDancerName.append(_add_name)
            if _update_age is not None:
                self.hasDancerAge=_update_age
            

with onto:
    class Hastamudra(Thing):
        @classmethod
        def print_asamyukta(cls):
            print('ID\tName')
            for mudra in onto.AsamyuktaMudra.instances():
                print(str(mudra.hasMudraId)+'\t'+mudra.name)
        
        @classmethod
        def print_samyukta(cls):
            print('ID\tName')
            for mudra in onto.SamyuktaMudra.instances():
                print(str(mudra.hasMudraId)+'\t'+mudra.name)
                
def add_new_dancer_instance(_dancer_name,_dancer_age,_dancer_gender):
    onto = get_ontology("file://"+onto_filepath).load()
    existing_dancers=onto.Dancer.instances()
    new_dancer=onto.Dancer('Dancer'+str(len(existing_dancers)),hasDancerId=len(existing_dancers))
    new_dancer.hasDancerName.append(_dancer_name)
    new_dancer.hasDancerAge = _dancer_age
    if _dancer_gender==0:
        new_dancer.hasDancerGender='M'
    elif _dancer_gender==1:
        new_dancer.hasDancerGender='F'
    else:
        new_dancer.hasDancerGender='O'
    onto.save(file = onto_filepath, format = "rdfxml")
    return new_dancer

def add_new_image_instance(image_path):
    l=image_path.split('/')
    file_fullname=l[len(l)-1]
    l=file_fullname.split('.')
    file_name=l[0]
    file_exten=l[1]
    file_size=os.path.getsize(image_path)
    m=len(onto.Image.instances())
    img=onto.Image('Image'+str(m),namespace=onto,hasFilePath=image_path,hasFileName=file_name,hasFileExtension=file_exten,hasFileSize=file_size)
    onto.save(file=onto_filepath,format="rdfxml")
    return img

def add_new_static_instance(_dance_name, _is_samyukta=False, _samyukta=None, _left=None, _right=None):
    existing_static=onto.Static.instances()
    static_desc=onto.Static('Static'+str(len(existing_static)))
    static_desc.hasDanceName.append(_dance_name)
    if _is_samyukta:
        static_desc.hasSamyuktaMudra=onto.search_one(hasMudraId=_samyukta)
    else:
        static_desc.hasLeftHandMudra=onto.search_one(hasMudraId=_left)
        static_desc.hasRightHandMudra=onto.search_one(hasMudraId=_right)
    onto.save(file = onto_filepath, format = "rdfxml")
    return static_desc

def add_new_content_instance(_image_instance,_dancer_instance,_static_instance):
    existing_content=onto.Content.instances()
    new_content=onto.Content('Content'+str(len(existing_content)))
    new_content.hasImage=_image_instance
    new_content.hasDancer.append(_dancer_instance)
    new_content.hasStatic=_static_instance
    onto.save(file = onto_filepath, format = "rdfxml")
    return new_content


    
def annotate_img_terminalUI():
    
    print('++ Add image ++')
    image_path=input('\__ Enter image path: ')
    image_added=add_new_image_instance(image_path)
    img=PIL.Image.open(image_path)
    img.show()
    
    print()
    
    print('++ Choose/Add dancer ++')
    print('List of recorded dancers: ')
    onto.Dancer.print_instances()
    if input('\__ Choose dancer from the list of pre-recorded dancers (Y/N): ').lower()=='y':
        _dancer_id=int(input('\__ Enter DancerId (refer to the list): '))
        dancer_in_image=onto.search_one(hasDancerId=_dancer_id)
        if input('\__ Update Dancer name (Y/N): ').lower()=='y':
            updated_name=input('\__ Enter updated name: ')
            dancer_in_image.update_dancer_info(_add_name=updated_name)
    else:
        new_dancer_name=input('\__ Enter dancer name: ')
        new_dancer_age=int(input('\__ Enter dancer age: '))
        new_dancer_gender=int(input("\__ Enter dancer gender ('0' for Male, '1' for Female, '2' for Others): "))
        dancer_in_image=add_new_dancer_instance(new_dancer_name,new_dancer_age,new_dancer_gender)
        
    print()
    
    print('++ Add static description ++')
    dance_name=input('\__ Enter dance name: ')
    if (input("Press 'A' for Asamyukta mudra and 'S' for Samyukta mudra: ")).lower()=='a':
        print('List of Asamyukta mudra: ')
        onto.Hastamudra.print_asamyukta()
        left_mudra=int(input('\__ Enter hastamudra ID performed on left hand (refer to list for ID): '))
        right_mudra=int(input('\__ Enter hastamudra ID performed on right hand (refer to list for ID): '))
        static_desc_image=add_new_static_instance(_dance_name=dance_name,_left=left_mudra,_right=right_mudra)
    else:
        print('List of Samyukta mudra: ')
        onto.Hastamudra.print_samyukta()
        mudra=int(input('\__ Enter samyukta mudra ID (refer to list for ID): '))
        static_desc_image=add_new_static_instance(_dance_name=dance_name,_is_samyukta=True,_samyukta=mudra)
    
    print()

    new_content=add_new_content_instance(image_added,dancer_in_image,static_desc_image)        
    
def main():
    annotate_img_terminalUI()
    
if __name__=='__main__':
    main()
