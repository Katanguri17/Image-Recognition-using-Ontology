# Project Title

We have designed an Ontology based Video Retrieval System.An ontology-based knowledge representation could be used for content analysis and concept recognition, for reasoning
processes and for enabling user-friendly and intelligent multimedia content
search and retrieval.

## Following is a description of:

1. Dependencies
2. Repository structure
3. Purpose, input, output of each file and its functions

## Dependencies:

inflect==5.6.2
nltk==3.7
Owlready2==0.38
pandas==1.4.2
Pillow==9.2.0
spacy==3.4.0

## Repository structure:
.
├── ontology_editing
├── NLP
└── data

## ONTOLOGY:

The domain knowledge related to hastamudra is maintained as an **OWL ontology**. It is stored in **rdfxml** format as dance_image_ontology.owl. The ontology IRI is: [http://www.semanticweb.org/rounak/ontologies/2022/5/dance_image_ontology](http://www.semanticweb.org/rounak/ontologies/2022/5/dance_image_ontology). The ontology is developed using **Protégé**. The different classes with their descriptions and properties are:

![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2010-54-17.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-35-36.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-35-58.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-36-24.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-36-53.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-37-15.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-39-24.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-39-24.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2022-39-41.png)

Note that all data properties **except hasDancerName and hasDanceName are functional** i.e every Dancer/Dance can be related to multiple data members by these properties (i.e. each dancer/dance individual can known and indentified by multiple names)

write here ontology_editing tree

## ontology_editing

./ontology_editing

### OntoEditModule.py (OEM):

Contains functions necessary to load the ontology as Python object, modify and save it, which are imported in AddImageAnnotationGUI.py. OEM makes use of Owlready2.0 package.
OEM also provides a terminal based UI in the form of the function annotate_img_terminalUI() for image annotation.

#### Execution 

Go to ontology_editing and run

```
	python3 OntoEditModule.py 
```

### AddImageAnnotationGUI.py:

Provides a GUI for convenient image annotation. Uses Python's Tkinter framework. It contains code to create the widgets for taking different annotations as input and imports the functions from OntoEditModule(OEM) to save those annotations in the ontology file.

#### Execution

Go to ontology_editing directory and run 
```
	python3 AddImageAnnotationGUI.py
```

### Dancer Details section:

#### Select Dancer from records:

Lets you chose a dancer from the list of dancers who are already present in the ontology through a dropdown menu.
Also possible to enter a new DancerName that will be appended to the list of names of the chosen dancer.

#### Add new dancer:

Create a new dancer individual (different from any other previously entered dancer in the ontology), with name, age and gender as input.

#### Enter dance name:

For hastamudra annotation, it is allowed to enter either one Samyukta hastamudra from the dropdown or two asamyukta mudras for left and right hand respectively

![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2010-52-16.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2010-53-00.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2010-53-24.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2010-53-55.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2010-54-17.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/Screenshot%20from%202022-07-29%2011-12-34.png)


### OntoQueryModule.py (OQM):

Contains functions for generating **SPARQL** queries given the requirements of the search.
We define two kinds of queries here: 
1. **Tight queries**: In this type of query the requirements of search are very clearly specified. The requirements are in the form of a dictionary which explicitly specifies the different fields like name, age, gender of dancer, dance name and hastamudra (If any of these fields are not necessary condition for filtering, that is assigned None). A typical requirements dictionary is like: 
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
(all images satisfying the None conditions should be retrieved by the query, note that any dictionary which mentions contradictory requirements like mentioning both sam_mudra and l_mudra is considered invalid)

2. **Open queries**: In this type of query, the requirements are in the form of a natural language text. Due to the difficulty in accurately being able to determine the requirements from free-form text, there is a relaxation provided while generating the SPARQL query. Therefore the task is to determine which keyword mentions which requirement (in terms of dancer details like gender, hastamudra etc) as much accurately as possible. This comes under **Named Entity Recognition** which is essentially a NLP problem.

Example: Consider the search string- '*** Show me a picture of male performing ordhapataka on left hand and alapada on right hand with vira rasa ***'

We should be able to detect the keyword 'male' and relate with the gender of the dancer and 'ordhapataka', 'alapada' as hastamudra keywords (Note that there may be random spelling mistakes in the search string, there is no hastamudra named 'ordhapataka' or 'alapada' in the ontology, so after detecting that these keywords represent hastamudra, we should be able to determine which valid hastamudra(s) is the most likely match).

Functions defined in OntoQueryModule.py are imported in QueryGUI.py.

### QueryGUI.py:

Provides a GUI for convenient searching. Uses Python's Tkinter framework. It contains code to create the widgets for taking input and imports the functions from OntoQueryModule(OEM) to save those annotations in the ontology file.

Allows making a tight query (fill in the entries for generating the requirements dictionary)
Or an open query by a single piece of text

#### Execution
Go to ontology_editing directory and run 
```
	python3 QueryGUI.py
```

![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/example_query_use_cases/Screenshot%20from%202022-07-29%2023-25-01.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/example_query_use_cases/Screenshot%20from%202022-07-29%2023-26-25.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/example_query_use_cases/Screenshot%20from%202022-07-29%2023-41-10.png)
![ScreenShot](https://github.com/rounaksaha12/Ontology-editing-and-Query-processing/blob/main/screenshots_to_add/example_query_use_cases/Screenshot%20from%202022-07-29%2023-41-49.png)

When the user makes an open query, (s)he is given the option to manually annotate the text he entered for the query. It has nothing to to with how the results of this particular query is executed. But a user-entered search text is a potentially useful data sample and if (s)he choses to help up by annotating it, the search text along with the annotations are safely stored within a binary file called 'unlearnt_bin' in the NLP directory. Samples present in this file represent data that is available but hasn't yet been used to train our NER model. The count of such samples is stored in hidden file '.unlearnt_samples_cnt.txt' within the same directory. NLP directory also contains an executable python script ***train_NLP_model.py*** which can be used to train the model with these unlearnt samples followed by which 'unlearnt_bin' is cleaned and unlearnt samples count is reduced to 0.

## NLP

./NLP
├── custom_nlp_for_dance
├── train_NLP_model.py
├── generate_query_dataset.py
├── dataset_bin
└── unlearnt_bin

The spaCy library provides features for Named Entity Recognition. However the pre-trained pipelines aren't fully suitable for our problem, since all the bharatnatyam and hastamudra specific terminology in general are not standard English words. However the NER pipeline can be trained for custom purposes with sufficient annotated dataset. Since no such dataset is readily available we have tried to automate the process of generating sample queries of some specific structures along with annotations.

### custom_nlp_for_dance:

spaCy NLP object trained with data samples generated by generate_query_dataset.py saved into memory, no need to train it everytime it is required, can be directly loaded from here

### generate_query_dataset.py:

Provides functions to generate and save random datasets for training NER model.
#### Execution: 
Go to NLP directory and run
```
	python3 generate_query_dataset.py
```
**This file is not meant to be run directly, anyway for test purposes running the above command generates 100 new data samples and saves them.**
	
### train_NLP_model.py(train):

Executable python script for training and saving spaCy nlp object. Input is train (list of training examples)

#### commandline options:

* -q, --query
	print the number of datasamples not yet used for training the nlp model
* -r, --random_learn sample_cnt
	randomly generate sample_cnt number of data samples through generate_query_dataset.py and train the nlp model
* -l, --learn_rem_samples
	prepares training data by mixing unlearnt data samples with equal number of randomly generated data samples(generated using generate_query_dataset.py) and trains the nlp model with that, the samples in unlearnt_samples.py are removed and the counter in .unlearnt_samples_cnt.txt is made 0

#### Execution

Go to NLP directory and run
```
	./train_NLP_model.py -q
```
for count of unlearnt samples

```
	./train_NLP_model.py -r 100
```
To train with 100 randomly generated data samples

```
	./train_NLP_model.py -l
```
To train with unlearnt samples mixed with random samples 
