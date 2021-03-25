import time
import subprocess as sp
import sys
from datetime import datetime
import re



#get docker image id as $ARGV[0];
imageid = sys.argv[1]
cmd_docker =  sp.getoutput("docker images -a | grep {0}| awk '{{print $2}}' ".format(imageid)).split("\n")
print(cmd_docker)




regex = re.compile(r'(\d).(\d).(\d)-(\d+)-(\w+)')
filtered = [i for i in cmd_docker if not regex.match(i)]

regex = re.compile(r'^[0-9]{1}.[0-9]{1}.[0-9]+-[0-9]+?$')
filtered = [i for i in filtered if not regex.match(i)]

regex = re.compile(r'^[0-9]{1}\.[0-9]{1}\.[0-9]+$')
filtered = [i for i in filtered if not regex.match(i)]
print(filtered)

regex = re.compile(r'(\d{2})(\d{2})(\d{2})')
filtered = [i for i in filtered if regex.match(i)]
print(filtered)


print(filtered[-2])

targetdates = [];

def parseDate(name) :
    s=str(name) #str conversion converts date ddmmyy to ['d','d','m','m','y','y']
    dd=s[0:2]
    mm=s[2:4]
    yy=s[4:]
    date_time=dd+'.'+mm+'.'+yy
    pattern="%d.%m.%y"
    epoch=int(time.mktime(time.strptime(date_time,pattern)))
    return epoch

beforeepoch=parseDate(filtered[-2])
#print(beforeepoch)
#print(beforeepoch)

def returnDate(epoch) :
    #This method converts epoch seconds to ddmmyy format to get the tag id      
    dddate=datetime.fromtimestamp(epoch).strftime("%d%m%y")
    return dddate

afterepoch=returnDate(beforeepoch)

for date in filtered:
    dateepoch = parseDate(date);
    if ( dateepoch < beforeepoch ) :
        targetdates.append(returnDate(dateepoch));

for targetdate in targetdates :
    #run docker rmi -f imageid:tag to untag the images with tag in $targetdate
     sp.getoutput("docker rmi -f {0}:{1}".format(imageid,targetdate))

images_left = sp.getoutput("docker images -a")
print("Images left for imageid:"+"\n"+images_left)


