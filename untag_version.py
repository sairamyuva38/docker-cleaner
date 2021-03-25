import os
import subprocess as sp
import sys
import re

imageid = sys.argv[1]

tagids = sp.getoutput("docker images -a | grep {0}| awk '{{print $2}}' ".format(imageid)).split("\n")
print(tagids)

regex = re.compile(r'(\d).(\d).(\d)-(\d+)-(\w+)')
filtered = [i for i in tagids if not regex.match(i)]
#print(filtered1)

regex = re.compile(r'(\d{2})(\d{2})(\d{2})')
filtered = [i for i in filtered if not regex.match(i)]


regex = re.compile(r'^[0-9]{1}.[0-9]{1}.[0-9]+-[0-9]+?$')
filtered1 = [i for i in filtered if regex.match(i)]


regex = re.compile(r'^[0-9]{1}\.[0-9]{1}\.[0-9]+$')
filtered2 = [i for i in filtered if regex.match(i)]
print(filtered2)
print(filtered1)



def matchversiontagsandseperate(name):
    l1=[]
    for i in name:
        l1.append(str(i)[4:])
    print(l1)


    l2=[]

    for i in filtered2:
        l2.append(str(i)[:3])
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
        if(tagid < target):
            print(tagid+"\n")
            targettags.append(tagid)

    for targettag in targettags :
        #run docker rmi -f imageid:tag to untag the images with tag in $targetdate
        for x in l2:
            originaltag = x + "." + targettag
            print(originaltag)
            sp.getoutput("docker rmi -f {0}:{1}".format(imageid,originaltag))

 

    imagesleft = sp.getoutput("docker images -a")
    print( "Images left for imageid:"+"\n"+imagesleft)

matchversiontagsandseperate(filtered1)
matchversiontagsandseperate(filtered2)

