f=open('dancer_list.tsv','w')
f.write('Dancer\tName\tAge\tGender\n')
for i in range(10):
	if i%2:
		G='M'
	else:
		G='F'
	f.write('Dancer'+str(i)+'\td'+str(i)+'\t'+str(20+i)+'\t'+G+'\n')
	
f.close()

f=open('costume_list.tsv','w')
f.write('Costume\n')
for i in range(5):
	f.write('Costume'+str(i)+'\n')
f.close


