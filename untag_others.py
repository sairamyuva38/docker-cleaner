import os
import subprocess as sp
import sys
import re

imageid = sys.argv[1]
#print(imageid)

imageid2 = sys.argv[2]
#print(imageid2)


tagids=sp.getoutput("docker images -a | grep {0}| awk '{{print $2}}' ".format(imageid)).split("\n")
#print(tagids)

regex = re.compile(r'(\d).(\d).(\d)-(\d+)-(\w+)_(\d+)')
filtered1 = [i for i in tagids if regex.match(i)]


for x in filtered1:
    sp.getoutput("docker rmi -f {0}:{1}".format(imageid,x))


imagesleft = sp.getoutput("docker images -a")
print( "Images left for imageid:"+"\n"+imagesleft)



tagids=sp.getoutput("docker images -a | grep {0}| awk '{{print $2}}' ".format(imageid)).split("\n")
#print(tagids)


regex = re.compile(r'(\d{2})(\d{2})(\d{2})')
tagids = [i for i in tagids if not regex.match(i)]
#print(tagids)



regex = re.compile(r'^[0-9]{1}.[0-9]{1}.[0-9]+-[0-9]+?$')
tagids = [i for i in tagids if not regex.match(i)]
#print(tagids)


regex = re.compile(r'^[0-9]{1}\.[0-9]{1}\.[0-9]+$')
tagids = [i for i in tagids if not regex.match(i)]
print(tagids)


regex = re.compile(r'(\w+)$')
tagids = [i for i in tagids if not regex.match(i)]
print(tagids)

matches = []
matches1 = []

for tag in tagids:
    if imageid2 in tag:
        matches.append(tag)
    else:
        matches1.append(tag)

print(matches)
print(matches1)

for x in matches1:
    sp.getoutput("docker rmi -f {0}:{1}".format(imageid,x))

imagesleft = sp.getoutput("docker images -a")
print( "Images left for imageid:"+"\n"+imagesleft)




l1=[]
for i in matches:
    l1.append(str(i)[6:9])
print(l1)

l2=[]
for i in matches:
    l2.append(str(i)[:5])
print(l2)

def get_unique_numbers(unsortedlist):
    list_of_unique_numbers = []
    unique_numbers = set(unsortedlist)
    for number in unique_numbers:
        list_of_unique_numbers.append(number)
    return list_of_unique_numbers

tagidunique=[]
tagidunique=get_unique_numbers(l1)


tagidsorted = []
tagidssorted=sorted(tagidunique)
print(tagidssorted)


target = tagidssorted[-2]

targettags=[]

for tagid in tagidssorted :
    print(tagid)
    if((tagid) < (target)):
        print(tagid + "\n")
        targettags.append(tagid)
print(targettags)

for targettag in targettags :
        for x in l2:
            originaltag = x+"-"+ targettag+"-"+imageid2
            sp.getoutput("docker rmi -f {0}:{1}".format(imageid,originaltag))


 

imagesleft = sp.getoutput("docker images -a")
print( "Images left for imageid:"+"\n"+imagesleft)

