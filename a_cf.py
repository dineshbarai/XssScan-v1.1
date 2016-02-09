import os,inspect
import re
import sys
from termcolor import colored
import colorama

colorama.init()

joint = 0
point = 0
class p_cf():
    def da_cf(self,post,rpn,cft,ref):
        global joint
        global point
        cft = cft.strip()
        regex = r'name\ *?=\ *?("|'+r"')"+cft+r'.*?>'
        token = re.search(regex,rpn,re.I|re.M)
        regex3 = r'(?<='+cft+r'\=).*?((?=")|(?=&)|(?=\s)|(?=$)|'+r"(?='))"
        token3 = re.search(regex3,rpn,re.I|re.M)
        post_regex = cft + r'(?=\=)'
        match_post = re.search(post_regex,post,re.I|re.M)
        if token:
            token1 = token.group()
            regex1 = r'(?<=value).*?("|' + r"').*?\1"
            token2 = re.search(regex1,token1,re.I|re.M)
            regex2 = r'(?<=("|' + r"')).*?(?=\1)"
            tokenvalue = re.search(regex2,token2.group(),re.I|re.M)
            token_regex = tokenvalue.group()
            token_regex = token_regex.strip("'")
            token_regex = token_regex.strip('"')
            token_regex = token_regex.replace(' ','+')
            if match_post:
                postdata = re.sub(r'(?<=('+cft+r'\=)).*?((?=&)|(?=\s)|(?=$))',token_regex,post,re.I|re.M)
                return postdata
            else:
                if point >=1:
                    return post
                print colored("\n---------------------------------------------------------------\nNo Anti CSRF token parameter '%s' found in Request.\nPress 'y' to continue without Anti-Csrf token or press 'n' to quit" %(cft),'yellow')
                while True:
                    try:
                        input = raw_input(colored("Press 'y' to continue or 'n' to quit...\n",'yellow'))
                    except KeyboardInterrupt, e:
                        print colored("\n---------------------------------------------------------------",'cyan')
                        print colored("Scanning interrupted",'red')
                    if input.lower() == 'y':
                        break
                    if input.lower() == 'n':
                        print colored("Scan result observed till now is stored in reflected.txt file",'yellow')
                        sys.exit(0)
                point +=1
                return post
        elif token3:
            if match_post:
                postdata = re.sub(r'(?<=('+cft+r'\=)).*?((?=&)|(?=\s)|(?=$))',token3.group(),post,re.I|re.M)
                return postdata
            else:
                if point >=1:
                    return post
                print colored("\n---------------------------------------------------------------\nNo Anti CSRF token parameter '%s' found in Request.\nPress 'y' to continue without Anti-Csrf token or press 'n' to quit\n" %(cft),'yellow')
                while True:
                    try:
                        input = raw_input(colored("Press 'y' to continue or 'n' to quit...\n",'yellow'))
                    except KeyboardInterrupt, e:
                        print colored("\n---------------------------------------------------------------",'cyan')
                        print colored("Scanning interrupted",'red')
                    if input.lower() == 'y':
                        break
                    if input.lower() == 'n':
                        print colored("Scan result observed till now is stored in reflected.txt file",'yellow')
                        sys.exit(0)
                point +=1
                return post    
        else:
            if joint >=1:
                return post
            print colored("\n---------------------------------------------------------------",'cyan')
            print colored("No Anti-CSRF token parameter '%s' found in Response.\nThe application usually logs out or produces error if proper Anti-Csrf token is not provided in request. This may result in improper scanning result.\nPress 'y' to continue without Anti-Csrf token or press 'n' to quit" %(cft),'white','on_red')
            while True:
                try:
                    input = raw_input(colored("\nPress 'y' to continue or 'n' to quit...\n",'yellow'))
                except KeyboardInterrupt, e:
                    print colored("\n---------------------------------------------------------------\n",'cyan')
                    print colored("Scanning interrupted\nExiting...",'red')
                    sys.exit(0)
                if input.lower() == 'y':
                    break
                if input.lower() == 'n':
                    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                    respfile = open(path+'/'+'resp.txt','w')
                    print "For details, refer the response stored in: resp.txt"
                    print colored("Scan result observed till now is stored in reflected.txt file",'yellow')
                    respfile.write(rpn)
                    respfile.close()
                    sys.exit(0)
            joint +=1
            return post