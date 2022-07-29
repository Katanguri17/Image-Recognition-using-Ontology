from nltk import edit_distance
import math


asam={
	('pataka',32): ['pataka','pathaka','potaka','potoka','ptka','ptk'],
	('tripataka',46): ['tripataka','tripathaka','thripathaka','tripotaka','tripotoka','trptka','trptk'],
	('ardhapatake',4): ['ardhapataka','ardhapathaka','ardhapotaka','ordhopotaka','adhapataka','adptka','adptk'],
	('kartari',18): ['kartari','karthari','kharthari','kortari','krtri'],
	('mayura',25): ['mayura','moyura','moyur','mayur','myur'],
	('ardhachandra',3): ['ardhachandra','adhachandra','ordhochondra','ordhochondro','adchnd'],
	('arala',2): ['arala','orola'],
	('shukatundaka',41): ['shukatundaka','shukhatundaka','sukatundaka','shukotundaka'],
	('mushti',28): ['mushti','musthi','mushthi','msthi'],
	('shikhara',39): ['shikhara','sikhara','shikara','sikara','shikhor','shkr'],
	('kapittha',15): ['kapittha','kopittha','kopitta','kpta'],
	('katakamukha',20): ['katakamukha','katakhamukha','kotokamukha','ktkmkh'],
	('suchi',43): ['suchi','shuchi','schi'],
	('chandrakala',8): ['chandrakala','chandhrakala','chandrakhala','chondrokola','chdrkla'],
	('padmakosha',30): ['padmakosha','podmokosha','padhmakhosha','padmakosha','pdmksh'],
	('sharpashirastatha',38): ['sharpashirastatha','shoropshirastatha','shrpsrsta'],
	('mrigashirsha',26): ['mrigashirsha','mrigoshirsho','mrigasirsha','mrgshrsha'],
	('singhamukha',42): ['singhamukha','singhomukha','singhamukho','snghmkh'],
	('kangula',14): ['kangula','khangula','kngl'],
	('alapadma',0): ['alapadma','alapadhma','olopoddo','olopodma','alpdm'],
	('chatura',9): ['chatura','chathura','chotur','chotura','chtr'],
	('bhramara',6): ['bhramara','bhromora','bhromor','bhrmr'],
	('hamsohasso',13): ['hamsohasso','hhmshs'],
	('hamsapakshaka',12): ['hamsapakshaka','hamshapakshaka','hamsapaksaka','hamsopokshoka','hmspksh'],
	('samdamsa',35): ['samdamsha','shamdamsa','smdmsh'],
	('mukula',27): ['mukula','mukhula','mhukula','mhukhula','mukul','mkl'],
	('tamrachura',45): ['tamrachura','tamrochura','tamrochuro','tmrchr'],
	('trishula',47): ['trishula','thrishula','thrisula','trishul','trshl'],
}

sam={
	('anjali',1): ['anjali','anjhali','onjoli','anjoli','anjhl'],
	('kapota',16): ['kapota','khapota','khaphota','kapotha','kpt'],
	('karkata',17): ['karkata','karkhata','kharkhata','kharkata','korkoto','krkt'],
	('swastika',44): ['swastika','swasthika','swastik','sostik','sstk'],
	('dolahasta',10): ['dolahasta','dholahstha','dholahasta','dolahosto','dlhst'],
	('pushpaputa',33): ['pushpaputa','pushphaputa','phuspoputa','pshpt'],
	('utsang',48): ['utsang','uthsang','utsng'],
	('shivalinga',40): ['shivalinga','shivalingha','sivalinga','siblingo','sblng'],
	('katakavardhana',21): ['katakavardhana','kathakavardhana','katakavardhan','kotokobordhon','ktkbrdhn'],
	('kartariswastika',19): ['kartariswastika','karthariswatika','kortarisostika','krtrswstk'],
	('sakata',34): ['sakata','sakhata','shakhata','sokota','sktk'],
	('shankha',37): ['shankha','sankha','shonkho','sonkho','snkh'],
	('chakra',7): ['chakra','chokro','chakhra','cakra','chkr'],
	('samputa',36): ['samputa','shamputa','somputa','smpt'],
	('pasha',31): ['pasha','pasa','phasa','phasha','phsh'],
	('kilakau',23): ['kilakau','khilakhau','kilakou','klkau'],
	('matsya',24): ['matsya','matshya','matsha','motsho','motso','mtsy'],
	('kurma',50): ['kurma','khurma','krm'],
	('baraha',5): ['baraha','boraho','bharaha','brh'],
	('garura',11): ['garura','gharura','gorura','grr'],
	('nagabandha',29): ['nagabandha','naghabandha','nhagabandha','nagbondho','ngbndh'],
	('khatawa',22): ['khatawa','khathawa','kthtw'],
	('verunda',49): ['verunda','vrnd'],

}

def match(keyword):
	match_a=[]
	match_s=[]
	min_d=math.inf

	for mudra in asam:
		d=min([edit_distance(keyword,instance) for instance in asam[mudra]])
		if d<min_d:
			min_d=d
			match_a.clear()
			match_a.append(mudra[1])
		elif d==min_d:
			match_a.append(mudra[1])

	for mudra in sam:
		d=min([edit_distance(keyword,instance) for instance in sam[mudra]])
		if d<min_d:
			min_d=d
			match_a.clear()
			match_s.clear()
			match_s.append(mudra[1])
		elif d==min_d:
			match_s.append(mudra[1])

	return match_a,match_s
            
