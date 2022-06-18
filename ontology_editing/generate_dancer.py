
f=open('dancer_list.tsv','w')
f.write('Dancer\tName\tAge\tGender\n')

for i in range(10):
	f.write('Dancer'+str(i+3)+'\td'+str(i+3)+'\t'+str(20+i)+'\t'+'F'+'\n')
	
f.close()
