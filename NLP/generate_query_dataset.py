import random

ask_keywords=[
    '','Get me','Get me an image','Get','Get an image', 'Show', 'Show me an image', 'Show me', 'Show me a picture', "Show a pic",
    "Fetch", "Fetch me a picture", "Fetch me an image", "Retrieve an image", "Retrieve", "Retrieve an instance"
]

filler_prep=['of', 'in which', 'where', 'which']

gender_keywords=['male','boy','man','he','mister',
'female','girl','woman','lady','she','miss']

gender_neutral=['dancer','performer','artist','expert','pandit']

hastamudra={
	'asamyukta': [
		'pataka',
		'tripataka',
		'ardhapatake',
		'kartari',
		'mayura',
		'ardhachandra',
		'arala',
		'shukatundaka',
		'mushti',
		'shikhara',
		'kapittha',
		'katakamukha',
		'suchi',
		'chandrakala',
		'padmakosha',
		'sharpashirastatha',
		'mrigashirsha',
		'singhamukha',
		'kangula',
		'alapadma',
		'chatura',
		'bhramara',
		'hamsohasso',
		'hamsapakshaka',
		'samdamsa',
		'mukula',
		'tamrachura',
		'trishula',
	],
	'samyukta':[
		'anjali',
		'kapota',
		'karkata',
		'swastika',
		'dolahasta',
		'pushpaputa',
		'utsang',
		'shivalinga',
		'katakavardhana',
		'kartariswastika',
		'sakata',
		'shankha',
		'chakra',
		'samputa',
		'pasha',
		'kilakau',
		'matsya',
		'kurma',
		'baraha',
		'garura',
		'nagabandha',
		'khatawa',
		'verunda',
	],
}

fac=['shringer','hasya','bibhatsya','rudra','shanta','veera','bhaya','karuna','advuta']

f=open('dataset.txt','w')

for i in range(100):
	text=""
	entities=[]
	choseGender=random.randint(0,3)
	isAsam=random.randint(0,1)
	mentionRasa=random.randint(0,4)

	text+=ask_keywords[random.randint(0,len(ask_keywords)-1)]
	if len(text):
		text+=" "
	if len(text):
		text+=filler_prep[random.randint(0,len(filler_prep)-1)]
		text+=" "
    
	if choseGender:
		start_gender=len(text)
		text+=gender_keywords[random.randint(0,len(gender_keywords)-1)]
		end_gender=len(text)
		entities.append((start_gender,end_gender,'GENDER'))
		text+=" performing "
	else:
		text+=gender_neutral[random.randint(0,len(gender_neutral)-1)]
		text+=" performing "

    
	if isAsam:
    	
		mentionLeft=random.randint(0,4)
		mentionRight=random.randint(0,4)
    	
		if mentionLeft:
			start_l_mud=len(text)
			text+=hastamudra['asamyukta'][random.randint(0,len(hastamudra['asamyukta'])-1)]
			end_l_mud=len(text)
			text+=" on left hand "
			entities.append((start_l_mud,end_l_mud,'MUDRA'))
			if mentionRight:
				text+="and "

		if mentionRight:
			start_r_mud=len(text)
			text+=hastamudra['asamyukta'][random.randint(0,len(hastamudra['asamyukta'])-1)]
			end_r_mud=len(text)
			text+=" on right hand "
			entities.append((start_r_mud,end_r_mud,'MUDRA'))
    	
	else:
    
		mentionAtAll=random.randint(0,4)
    	
		if mentionAtAll:
			start_s_mud=len(text)
			text+=hastamudra['samyukta'][random.randint(0,len(hastamudra['samyukta'])-1)]
			end_s_mud=len(text)
			text+=" "
			entities.append((start_s_mud,end_s_mud,'MUDRA'))



	if mentionRasa:
		text+="with "
		start_fac=len(text)
		text+=fac[random.randint(0,len(fac)-1)]
		end_fac=len(text)
		entities.append((start_fac,end_fac,'FAC'))
		if random.randint(0,3):
			text+=" rasa"
	
    
	f.write('("'+text+'", {"entities": ')
	f.write(str(entities)+'}),\n')
    
f.close()
