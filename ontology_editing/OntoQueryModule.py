from owlready2 import *
import spacy
import os
import MudraMatch

cwd = os.path.dirname(os.path.realpath('__file__'))
onto_filepath=cwd+r'/dance_image_ontology.owl'
onto = get_ontology('file://'+onto_filepath).load()

nlp=spacy.load(os.path.dirname(cwd)+r'/NLP/custom_nlp_for_dance')

init_query_str="""
PREFIX dio: <http://www.semanticweb.org/rounak/ontologies/2022/5/dance_image_ontology#>
SELECT DISTINCT ?image_path
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

def generate_requirements(free_form_text):
	doc=nlp(free_form_text)
	DancerName=None
	DancerGender=None
	AsamMudList=[]
	SamMudList=[]
	for ent in doc.ents:
		if ent.label_=='PERSON':
			DancerName=ent.text
		if ent.label_=='GENDER':
			if ent.text in ['male','boy','man','he','mister']:
				DancerGender='M'
			elif ent.text in ['female','girl','woman','lady','she','miss']:
				DancerGender='F'
		if ent.label_=='MUDRA':
			match_a,match_s=MudraMatch.match(ent.text.lower())
			# print(match_a,match_s)
			AsamMudList.extend(match_a)
			SamMudList.extend(match_s)
	return DancerName,DancerGender,AsamMudList,SamMudList


def generate_open_query(free_form_text):
	DancerName,DancerGender,AsamMudList,SamMudList=generate_requirements(free_form_text)
	query=init_query_str
	if DancerName is not None:
		query=query+"\tFILTER regex(?dancer_name,'"+DancerName+"','i')\n"
	if DancerGender is not None:
		query=query+"\tFILTER regex(?dancer_gender,'"+DancerGender+"','i')\n"

	if len(AsamMudList)>0:
		asam_filter_condition=""
		for mudra_id in AsamMudList:
			asam_filter_condition=asam_filter_condition+" ?l_mudra="+str(mudra_id)+" || ?r_mudra="+str(mudra_id)+" ||"
		asam_filter_condition=asam_filter_condition[:-2] # remove last '||'
		asam_query=query+"\t?static dio:hasLeftHandMudra/dio:hasMudraId ?l_mudra . \n"+"\t?static dio:hasRightHandMudra/dio:hasMudraId ?r_mudra . \n"
		asam_query=asam_query+"\tFILTER ("+asam_filter_condition+")\n"+'\t?image dio:hasFilePath ?image_path\n}\n'
	else:
		asam_query=None
	
	if len(SamMudList)>0:
		sam_filter_condition=""
		for mudra_id in SamMudList:
			sam_filter_condition=sam_filter_condition+" ?sam_mudra="+str(mudra_id)+" ||"
		sam_filter_condition=sam_filter_condition[:-2]
		sam_query=query+"\t?static dio:hasSamyuktaMudra/dio:hasMudraId ?sam_mudra . \n"
		sam_query=sam_query+"\tFILTER ("+sam_filter_condition+")\n"+'\t?image dio:hasFilePath ?image_path\n}\n'
	else:
		sam_query=None
	
	return asam_query,sam_query


def generate_tight_query(requirements):
    query=init_query_str
    
    if requirements['dancer_name'] is not None:
        query=query+"\tFILTER regex(?dancer_name,'"+requirements['dancer_name']+"','i')\n"
    if requirements['dancer_age'] is not None:
        query=query+"\tFILTER (?dancer_age = "+str(requirements['dancer_age'])+")\n"
    if requirements['dancer_gender'] is not None:
        query=query+"\tFILTER regex(?dancer_gender,'"+requirements['dancer_gender']+"','i')\n"
    
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
	print('+++ TIGHT QUERY +++')
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
	print('Requirements dict.:',requirements)
	query=generate_tight_query(requirements)
	l0=list(default_world.sparql(query))
	print('SPARQL query:')
	print(query,end='')
	print([ s[0][-7:] for s in l0])

	print('+++ OPEN QUERY +++')
	ex_free_form_text='Show me a picture of male performing ardhapataka on left hand and alapada on right hand with vira rasa'
	a,b=generate_open_query(ex_free_form_text)
	print('Query text:',ex_free_form_text)

	if a is not None:	
		print('Asamyukta mudra specific SPARQL query:')
		print(a,end='')
		l1=list(default_world.sparql(a))
		print([ s[0][-7:] for s in l1] )
	if b is not None:
		print('Samyukta mudra specific SPARQL query:')
		print(b,end='')
		l2=list(default_world.sparql(b))
		print([ s[0][-7:] for s in l2])
	
	
	

if __name__=='__main__':
	test()
