import urllib2, urllib
import re
import os, inspect
from o_n import onh
import sys
import time
import signal
import xyzs
import br_log
from r_p import f_p
from termcolor import colored
import colorama

colorama.init()
options = onh()
print colored("Disclaimer:",'blue','on_white') + colored(" Usage of XssScan tool for testing targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program\n",'cyan')
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ref_file = open(path+'/'+'reflected.txt','w')
ref_file.close()
f_parse = f_p()
def signal_handler(signal, frame):    
    print colored("\n---------------------------------------------------------------",'cyan')
    print colored("\nScanning interrupted\nExiting...\n",'red')
    print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
    if options.shreflected ==True:
        print colored("-----------------------Scan Results------------------------",'green','on_white')
        ref_file = open(path+'/'+'reflected.txt','r')
        print colored(ref_file.read(),'green')
        ref_file.close()
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

cr =0
r_count =0
a = xyzs.xss()

if options.burplogfile == None:
    try:
        req_file = open(path+'/'+options.request,'r')
    except IOError:
        print colored("Cannot read the request file '%s' in folder '%s'." %(options.request,path),'white','on_red')
        print colored("Exiting...",'red')
        sys.exit(0)
    postdata = req_file.read()
    if options.cookie !=None and options.cookie !='':
        postdata = f_parse.cookie(postdata,options.cookie)
    p = a.xssrun(postdata,'test',False)
    cr+=p
else:
    if options.csrftoken != None:
        print colored("Note that Anti-Csrf token replacement feature is disabled when reading requests through burp log or saved history file",'yellow')
        while True:
            try:
                input = raw_input(colored("Press 'y' to continue...\n",'yellow'))
            except KeyboardInterrupt, e:
                print colored("\n---------------------------------------------------------------",'cyan')
                print colored("Scanning interrupted\nExiting...",'red')
                sys.exit(0)
            if input.lower() == 'y':
                break
    burplog = br_log.brlg()
    for postdata,mode in burplog.parbrlg():
        if options.domain != None and options.domain != '':
            val = f_parse.domain(postdata, options.domain)
            if val == False:
                continue
        r_count +=1
        header,body,method,url = f_parse.f_par(postdata,mode)
        #print colored("\n=========================================================================",'cyan')
        print colored("#########################################################################",'cyan')
        print colored("Scanning request to url: %s\n" %(url),'yellow')
        ref_file = open(path+'/'+'reflected.txt','a')
        ref_file.write("===============================================================================\n")
        ref_file.write("Results for url " + url+"\n")
        ref_file.close()
        if options.cookie !=None and options.cookie !='':
            postdata = f_parse.cookie(postdata,options.cookie)
        p = a.xssrun(postdata,mode,True)
        cr +=p
if options.burplogfile != None:
    print colored("-----------------------------------------------------------\n",'cyan')
    print colored("Total %s HTTP requests were scanned from file '%s'\n" %(str(r_count),options.burplogfile),'yellow')
if cr >0:
    print colored("-----------------------------------------------------------\n",'cyan')
    print colored("REFLECTIONS WERE FOUND FOR SOME PAYLOADS",'green')
    print colored("DETAILS ARE STORED IN reflected.txt\n",'green')
else:
    print colored("-----------------------------------------------------------\n",'cyan')
    print colored("No reflections for any were found for any payload\n",'red')
    ref_file = open(path+'/'+'reflected.txt','w')
    ref_file.write("No reflections were found")
    ref_file.close()
if options.shreflected ==True:
    print colored("-----------------------Scan Results------------------------",'white','on_green')
    ref_file = open(path+'/'+'reflected.txt','r')
    if cr==0:
        print colored(ref_file.read(),'red')
    else:
        print colored(ref_file.read(),'green')
    ref_file.close()