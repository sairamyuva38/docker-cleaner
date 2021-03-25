#!/us/bin/python

import subprocess as sp
import sys,os
import re


cmd_docker = "docker images -a | grep 'acceldata' | awk '{{print $1}}' "
dates = sp.getoutput(cmd_docker).split("\n")

l=' '.join([str(elem) for elem in dates])



l2=[]
l3=[]

for x in dates:
    if x.startswith("acceldata") == True :
        l2.append(x)
    else :
        l3.append(x)

#removing the duplicates
unique_images_startswith_acceldata = set(l2)
unique_images_endswith_acceldata = set(l3)


#getting tags as list
image_to_tagmap = {}
datematch = {}
image2tag = {}


def matchtagsandseperate(images_dict):
    for imagename in images_dict:
        image_to_tagmap[imagename] = sp.getoutput("docker images | grep 'acceldata' | awk '{{print $2}}' ").split("\n")
        dates_list = [li for li in image_to_tagmap[imagename] if re.match(r'(\d{2})(\d{2})(\d{2})',li) ] 
        dates_tuple = tuple(dates_list)
        image2tag[dates_tuple]=imagename

        dob_list = [v for v in image_to_tagmap[imagename] if re.match(r'(\d).(\d).(\d)-(\d+)-(\w+)',v) ]
        dob_tuple = tuple(dob_list)
        image2tag[dob_tuple]=imagename
        
        os.system("python untag_date.py {0}".format(image2tag[dates_tuple])

matchtagsandseperate(unique_images_startswith_acceldata)
matchtagsandseperate(unique_images_endswith_acceldata)










