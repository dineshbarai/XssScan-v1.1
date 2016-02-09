import os,inspect
import sys
from termcolor import colored
import colorama

colorama.init()
class lgt:
    global path
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    def cklgt(self,data,lgts,lgtc,respcode,requrl,respurl,ref):
        if lgts!='' and lgts!=None:
            if data.find(lgts) >=0:
                print colored("\nThe string '%s' was encountered in response" %(lgts),'white','on_red')
                print colored("The application has logged out\n",'red')
                print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
                sys.exit(0)
        if lgtc!='' and lgtc!=None:
            if str(lgtc)[0] == '3':
                if requrl != respurl:
                    print colored("\nRedirection was observed to %s" %(respurl),'white','on_red')
                    print colored("The application has logged out\n",'red')
                    print colored("Scan result observed till now is stored in reflected.txt file",'yellow')
                    sys.exit(0)
            if str(respcode) == str(lgtc):
                print colored("\nResponse with code '%s' was observed" %(str(lgtc)),'white','on_red')
                print colored("The application has logged out\n",'red')
                print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
                sys.exit(0)