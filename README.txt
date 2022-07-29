./ontology_editing
├── dance_image_ontology.owl
├── OntoEditModule.py
├── AddImageAnnotationGUI.py
├── Pre_process.py
├── MudraMatch.py
├── OntoQueryModule.py
└── QueryGUI.py

OntoEditModule.py (OEM):
Contains functions necessary to load the ontology as Python object, modify and save it. OEM makes use of Owlready2.0 package. Functions provided by OEM:

1. def add_new_dancer_instance(_dancer_name,_dancer_age,_dancer_gender)
	# create an individual of Dancer class in the ontology with properties DancerName=[_dancer_name,], DancerAge=_dancer_age, DancerGender=_dancer_gender
	# note that hasDancerName property is not functional which means the same Dancer individual can have multiple names, and hence is stored as a list
	# allowing same dancer to have multiple names gives the advantage of identifying him/her with different names in different images, also ensures that while searching, an image featuring a particular dancer is retrieved irrespective of what name is used in the query(ofcourse the name needs to be a valid one)
	
2. def update_dancer_info(self, _add_name=None, _update_age=None) 
	# added as a member function of the Dancer class
	# if _add_name != None, it is appeneded to the list of names of the dancer individual
	# if _update_age != None, the age of the individual is modified to the argument 
	
3. def add_new_image_instance(image_path)
	# adds new individual of Image class, the datamembers are decidied(full name, image name, extension, size) are decided from the image_path
	
4. def add_new_static_instance(_dance_name, _is_samyukta=False, _samyukta=None, _left=None, _right=None)
	# adds a individual of the static class with DanceName=_dance_name, note that hasDanceName property is also not functional (same dance can be known by multiple names)
	# if _is_samyuta==True, the Static individual is assigned the samyukta mudra with MudraId=_samyukta
	# else, it is assigned asamyukta mudras for both left and right hand which have MudraId _left and _right respectively
	# note that the ontology has the restriction that the Static individual can have either 1 unambiguous Samyukta mudra OR a pair of 2 Asamyukta mudras for both hands
	# note that due to lack of domain knowledge we could not account for attributes like HeadPosition, LedPosition, TorsoPosition, though they are there in the ontology and can be extended by adding indiviuals of these classes. As of now we have created dummy(NULL) individuals of these classes and assigning them whenever new Static individual is created
	
5. def add_new_content_instance(_image_instance,_dancer_instance,_static_instance)
	# creates the outermost wrapper of an annotation,viz. an individual of the Content class with _image_instance(Image individual), _dancer_instance(Dancer individual), _static_instance(Static individual) 
	
OEM also provides a terminal based UI in the form of the function annotate_img_terminalUI() for image annotation

AddImageAnnotationGUI.py:
Provides a GUI for convenient image annotation. Uses Python's Tkinter framework. It contains code to create the widgets for taking different annotations as input and imports the functions from OntoEditModule(OEM) to save those annotations in the ontology file.

<explain diff entries from screenshots>

Dancer Details section:
Select Dancer from records:
Lets you chose a dancer from the list of dancers who are already present in the ontology through a dropdown menu.
Also possible to enter a new DancerName that will be appended to the list of names of the chosen dancer.
Add new dancer:
Create a new dancer individual (different from any other previously entered dancer in the ontology), with name, age and gender as input.

Dance Details section:
Enter dance name
For hastamudra annotation, it is allowed to enter either one Samyukta hastamudra from the dropdown or two asamyukta mudras for left and right hand respectively

MudraMatch.py:
The list of valid Hastamydras in bharatnatyam is finite, and hence can be listed down exhaustively. The ontology is loaded with 28 distinct Asamyukta mudras and 23 distinct Samyukta mudras. MudraMatch.py provides the function which decides, upon taking a free-form piece of text (a word or a phrase), which of the hastamudras in the ontology is closest match for the input. (Example: if input is 'shonkho mudra' hastamudra keywords with best syntactic match would be among 'shirsha', 'shikhara' mudras)
It maintains 2 lists(one for samyukta and another for asamyukta mudra) in the form of a dictionary where the (key,value) pair is of the form: ( (predefined hastamudra name,ID), a list of possible variations / misspellings of the name of the mudra).

asam={
	('pataka',32): ['pataka','pathaka','potaka','potoka','ptka','ptk'],
	('tripataka',46): ['tripataka','tripathaka','thripathaka','tripotaka','tripotoka','trptka','trptk'],
	.
	.
	.
	('tamrachura',45): ['tamrachura','tamrochura','tamrochuro','tmrchr'],
	('trishula',47): ['trishula','thrishula','thrisula','trishul','trshl'],
}

sam={
	('anjali',1): ['anjali','anjhali','onjoli','anjoli','anjhl'],
	('kapota',16): ['kapota','khapota','khaphota','kapotha','kpt'],
	.
	.
	.
	('khatawa',22): ['khatawa','khathawa','kthtw'],
	('verunda',49): ['verunda','vrnd'],
}

Explanation for match(keyword) function:
We go through each of the mudras (once through asam and then sam), for each mudra we find the similarity** of the keyword with each of the entries of the list(of possible variation/misspellings) and take the maximum which we consider as the overall Similarity of keyword with that particular mudra. We return the ID of mudra(s) with maximum overall Similarity. The function returns two lists match_a=[x for overall Similarity(x)==m and x is AsamyuktaMudra], match_s= [x for overall Similarity(x)==m and x is SamyuktaMudra] where m is the maximum overall similarity over all hastamudrs(asamyukta and samyukta combined).
(** measure of similarity: we use Levenstein(/edit) distance to measure the similarity between two words, lower the edit distance higher the similarity).

OntoQueryModule.py (OQM):
Contains functions for generating SPARQL queries given the requirements of the search.
We define two kinds of queries here: 
1. Tight queries: In this type of query the requirements of search are very clearly specified. The requirements are in the form of a dictionary which explicitly specifies the different fields like name, age, gender of dancer, dance name and hastamudra (If any of these fields are not necessary condition for filtering, that is assigned None). A typical requirements dictionary is like: 
requirements={
	'dancer_name': 'rahul' ,
	'dancer_id': None ,
	'dancer_age': None , 
	'dancer_gender': 'M' ,
		
	'dance_name': None ,
	'sam_mudra': None ,
	'l_mudra': 4 , # mudra id
	'r_mudra': None
}
(all images satisfying the non-None conditions should be retrieved by the query, note that any dictionary which mentions contradictory requirements like mentioning both sam_mudra and l_mudra is considered invalid)
2. Open queries: In this type of query, the requirements are in the form of a natural language text. Due to the difficulty in accurately being able to determine the requirements from free-form text, there is a relaxation provided while generating the SPARQL query. Therefore the task is to determine which keyword mentions which requirement (in terms of dancer details like gender, hastamudra etc) as much accurately as possible. This comes under Named Entity Recognition which is essentially a NLP problem.
Example: Consider the search string- 'Show me a picture of male performing ordhapataka on left hand and alapada on right hand with vira rasa'
We should be able to detect the keyword 'male' and relate with the gender of the dancer and 'ordhapataka', 'alapada' as hastamudra keywords (Note that there may be random spelling mistakes in the search string, there is no hastamudra named 'ordhapataka' or 'alapada' in the ontology, so after detecting that these keywords represent hastamudra, we should be able to determine which valid hastamudra(s) is the most likely match).

Functions provided by OQM:

def generate_tight_query(requirements)
	# takes a requirements dictionary as input and generates a SPARQL query string
The SPARQL query string generated from the tight requiremets dictionary mentioned while explaining tight query:
'''
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
	FILTER regex(?dancer_name,'rahul','i')
	?static dio:hasLeftHandMudra/dio:hasMudraId ?l_mudra . 
	FILTER (?l_mudra = 4)
    ?image dio:hasFilePath ?image_path
}
'''

def generate_requirements(free_form_text)
	# recognizes named entities from natural language text, finds closest match of hastamudra keywords recognized in the text with list of hastamudras defined in the ontology and returns the requirements in the form of DancerName,DancerGender,AsamMudList(list of closest asamyukta mudras),SamMudList(list of closest samyukta mudras)
	# uses NLP pipeline provided by the Python library spaCy and trained with natural language queries related to hastamudra for named entity recognition (more details in NLP directory) and MudraMatch.py (MM) for finding closest match

def generate_open_query(free_form_text)
	# calls generate_requirements(free_form_text) for determining the requirements, then constructs the SPARQL query 
	# note that presence of both samyukta mudra and asamyukta mudra in the requirements wont be considered contractory as it would have been for a tight query. Here the hastamudra requirements are conjuncted by OR (||) i.e any image which contains any of the detected mudras (samyukta or asamyukta mudra) in any of the hands will be retrieved. This relaxation has been done considering the limited accuracy of our NER model (due to limited quantity and variety of dataset).
	# two different SPARQL queries are generated: one filtering by the OR-ed list of closest samyukta mudra and asamyukta mudra for the other. 
The SPARQL query string generated from free-form text mentioned while explaining open query:

(asamyukta mudra specific)
'''
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
	?static dio:hasLeftHandMudra/dio:hasMudraId ?l_mudra . 
	?static dio:hasRightHandMudra/dio:hasMudraId ?r_mudra . 
	FILTER ( ?l_mudra=4 || ?r_mudra=4 || ?l_mudra=0 || ?r_mudra=0 )
    ?image dio:hasFilePath ?image_path
}
'''

(samyukta mudra specific)
'''PREFIX dio: <http://www.semanticweb.org/rounak/ontologies/2022/5/dance_image_ontology#>
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
	FILTER regex(?dancer_name,'rahul','i')
	?static dio:hasLeftHandMudra/dio:hasMudraId ?l_mudra . 
	FILTER (?l_mudra = 4)
    ?image dio:hasFilePath ?image_path
}
'''

QueryGUI.py:
Provides a GUI for convenient searching. Uses Python's Tkinter framework. It contains code to create the widgets for taking input and imports the functions from OntoQueryModule(OEM) to save those annotations in the ontology file.
Allows making a tight query (fill in the entries for generating the requirements dictionary)
Or an open query by a single piece of text

<screenshots>

./NLP
├── custom_nlp_for_dance
├── train_NLP_model.py
├── generate_query_dataset.py
├── dataset_bin
└── unlearnt_bin

The spaCy library provides features for Named Entity Recognition. However the pre-trained pipelines aren't fully suitable for our problem, since all the bharatnatyam and hastamudra specific terminology in general are not standard English words. However the NER pipeline can be trained for custom purposes with sufficient annotated dataset. Since no such dataset is readily available we have tried to automate the process of generating sample queries of some specific structures along with annotations.

custom_nlp_for_dance:
spaCy NLP object trained with data samples generated by generate_query_dataset.py saved into memory, no need to train it everytime it is required, can be directly loaded from here

generate_query_dataset.py:
def save_dataset(n)
	# Generates a set of n sample queries broadly in the below format: 
	# calls active_query() with probability 0.5 that generates query of the form: (verbs like 'retrieve'/'get'/'show')-(dancer name/gender specific noun or pronoun/gender neutral noun)-(action verb like 'performing','doing','acting')-(asamyukta mudra performed in one hand/both hands/samyukta mudra/no mudra information at all)-(keyword mentioning facial expression)
	# calls passive_query() rest of the time that generates query of the form: (asamyukta mudra performed in one hand/both hands/samyukta mudra/no mudra information at all)-(action verb like 'performed by','acted by')-(dancer name/gender specific noun or pronoun/gender neutral noun)-(keyword mentioning facial expression)
	# choseGender = random.randint(0, 3)choses gender specifying keyword with prob 0.75, gender neutral keywords rest of the time
    	# isAsam = random.randint(0, 1)choses asamyukta mudra with prob 0.5, samyukta mudra rest of the time
    	# saves the list of generated samples in a binary file 'dataset_bin'
    	# generated dataset is of the form:
    	# [
    	# ("get me an image where man performing with bhaya rasa", {"entities": [(22, 25, 'GENDER'), (42, 47, 'FAC')]}),
	# ("anjali mudra shown by man dancer with hasya rasa", {"entities": [(0, 6, 'MUDRA'), (22, 25, 'GENDER'), (38, 43, 'FAC')]}),
	# ("samdamsa on left hand demonstrated by pandit ", {"entities": [(0, 8, 'MUDRA')]}),
	# ...
	# ]
	
train_NLP_model.py(train):
python script for training and saving spaCy nlp object. Input is train (list of training examples)
commandline options:
-r, --random_learn sample_cnt: randomly generate sample_cnt data samples through generate_query_dataset.py and train the nlp model
