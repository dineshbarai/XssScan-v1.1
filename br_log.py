import re
import os,inspect
from o_n import onh
import sys
import base64
from termcolor import colored
import colorama


colorama.init()
options = onh()
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if options.burplogfile !=None:
    try:
        req_file = open(path+'/'+options.burplogfile,'r')
        data = req_file.read()
        regex = r'={10,}\s+[^=]+={10,}\s(.+?)\s={10,}'
        regex1 = r'<port>(\d+)</port>.+?<request base64="true"><!\[CDATA\[([^]]+)'
        comp = re.compile(regex,re.I|re.S)
        comp1 = re.compile(regex1,re.I|re.S)
        fil = re.search(regex,data,re.I|re.S)
        fil1 = re.search(regex1,data,re.I|re.S)
    except IOError:
        print colored("Cannot read the request file '%s' in folder '%s'." %(options.burplogfile,path),'white','on_red')
        print colored("Exiting...",'red')
        sys.exit(0)

class brlg:
    def parbrlg(self):
        global comp
        global comp1
        global data
        global fil
        global fil1
        if fil:
            for match in comp.finditer(data):
                postdata = match.group().splitlines()
                a = postdata[1]
                mode = re.search(r'(?<= )\w+?(?=://)',a,re.I)
                del postdata[0]
                del postdata[0]
                del postdata[0]
                del postdata[len(postdata)-1]
                postdata = "\r\n".join(postdata)
                yield postdata,mode.group()
        elif fil1:
            for match in comp1.finditer(data):
                regex2 = r'<request.*'
                match1 = re.search(regex2,match.group(),re.I|re.S)
                regex3 = r'(?<=CDATA\[).*'
                match2 = re.search(regex3,match1.group(),re.I|re.S)
                try:
                    postdata = base64.b64decode(match2.group())
                except:
                    postdata = match2.group()
                regex4 = r'(?<=<protocol>)\w+'
                match3 = re.search(regex4,match.group(),re.I|re.M)
                mode = match3.group()
                yield postdata,mode
        else:
            print  colored("Burpsuite log or history not in proper format. Kindly check the log file.",'white','on_red')
            sys.exit(0)