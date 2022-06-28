from owlready2 import *
import os

onto_filepath='/home/swarup3204/Ontology-editing-and-Query-processing/ontology_editing/dance_dummy.owl'
onto = get_ontology('file://'+onto_filepath).load()

def generate_requirements(free_form_text):
	pass

def generate_query(requirements):
    query="""
    PREFIX dio: <http://www.semanticweb.org/rounak/ontologies/2022/5/dance_image_ontology#>
    SELECT ?image_path
    WHERE{
        ?content a dio:Content ;
            dio:hasDancer ?dancer ;
            dio:hasStatic ?static ;
            dio:hasImage ?image .
        ?dancer dio:hasDancerName ?dancer_name ;
            dio:hasDancerAge ?dancer_age ;
            dio:hasDancerId ?dancer_id ;
            dio:hasDancerGender ?dancer_gender .
        ?static dio:hasDanceName ?dance_name .
    """
    
    if requirements['dancer_name'] is not None:
        query=query+"\tFILTER regex(?dancer_name,'"+requirements['dancer_name']+"','i')\n"
    if requirements['dancer_age'] is not None:
        query=query+"\tFILTER (?dancer_age = "+str(requirements['dancer_age'])+")\n"
    if requirements['dancer_gender'] is not None:
        query+query+"\tFILTER regex(?dancer_gender,'"+requirements['dancer_gender']+"','i')\n"
    
    if requirements['dance_name'] is not None:
        query=query+"\tFILTER regex(?dance_name,'"+requirements['dance_name']+"','i')\n"
    if requirements['sam_mudra'] is not None:
        query=query+"\t?static dio:hasSamyuktaMudra/dio:hasMudraId ?sam_mudra . \n"
        query=query+"\tFILTER (?sam_mudra = "+str(requirements['sam_mudra'])+")\n"
    if requirements['l_mudra'] is not None:
        query=query+"\t?static dio:hasLeftHandMudra/dio:hasMudraId ?l_mudra . \n"
        query=query+"\tFILTER (?l_mudra = "+str(requirements['l_mudra'])+")\n"
    if requirements['r_mudra'] is not None:
        query=query+"\t?static dio:hasRightHandMudra/dio:hasMudraId ?r_mudra . \n"
        query=query+"\tFILTER (?r_mudra = "+str(requirements['r_mudra'])+")\n"
    
    query=query+'?image dio:hasFilePath ?image_path\n}\n'
    return query

def test():
	requirements={
		# dancer details
		'dancer_name': 'rahul' ,
		'dancer_id': None ,
		'dancer_age': None , 
		'dancer_gender': 'M' ,
		
		#dance_details
		'dance_name': None ,
		'sam_mudra': None ,
		'l_mudra': 4 ,
		'r_mudra': None
	}
	query=generate_query(requirements)
	print(list(default_world.sparql(query)))

if __name__=='__main__':
	test()