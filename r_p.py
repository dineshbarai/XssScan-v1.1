import re
from re import sub,search,match
import os, inspect
import sys
from termcolor import colored
import colorama

colorama.init()

class f_p:
    global CRLF
    CRLF = '\r\n\r\n'
    def f_par(self,post,mode):
        global CRLF
        post = post + '\r\n\r\n'
        post = re.sub(r'\r?\n\r?\n\r?\n\r?\n',r'\r\n\r\n',post,re.I|re.M|re.S)
        h_p = r'.*?(?=(\r?\n\r?\n))'
        d_p = r'((?<=(\n\n))|(?<=(\r\n\r\n))).*'
        hd = search(h_p,post,re.I|re.M|re.S)
        bd = search(d_p,post,re.I|re.M|re.S)
        b=hd.group()
        bd = bd.group().rstrip()
        hrs = []
        regex = re.compile(r'^.*$',re.I|re.M)
        
        for match in regex.finditer(b):
            hrs.append(match.group())
        f_l = hrs[0] 
        del hrs[0]
        length = len(hrs)
        h_t ={}
        try:
            for count in range(0,length):
                sp = hrs[count].split(':',1)	
                h_t[sp[0].rstrip()] = sp[1]
        except IndexError:
            print colored("\nHttp request not in proper format.",'white','on_red')
            print "Kindly check the http request file.\nIf the file contains burplog or burp history, use -b option instead.\nExiting..."
            sys.exit(0)
        method = f_l.split(' ',1)[0]
        if 'Host' in h_t:
            url1 = h_t['Host'].replace("http://",'').replace("https://",'')
            h_t['Host'] = url1
            url = url1.lstrip().rstrip()+f_l.split()[1].lstrip()
        elif 'host' in h_t:
            url1 = h_t['host'].replace("http://",'').replace("https://",'')
            h_t['host'] = url1
            url = url1.lstrip().rstrip()+f_l.split()[1].lstrip()
        else:
            print colored("\nHost header not found in http request file.",'white','on_red')
            print colored("\nExiting...",'red')
            sys.exit(0)
        mode = mode.lower()
        if mode == 'http':
            url = 'http://'+ url
            url = url.replace(' ','+')
            url = url.replace('#',r'%23')
        elif mode =='https':
            url = 'https://'+ url
            url = url.replace(' ','+')
            url = url.replace('#','%23')
        else:
            print colored("Please select mode between HTTP or HTTPS",'white','on_red')
            sys.exit(0)
        return h_t,bd,method,url

    def c_l(self,post):
        global CRLF
        post = post + CRLF
        post = re.sub(r'\r?\n\r?\n\r?\n\r?\n',r'\r\n\r\n',post,re.I|re.M|re.S)
        len1 = re.search(r'((?<=(\r\n\r\n))|(?<=(\n\n)))^.*((?=(\n\n))|(?=(\r\n\r\n)))',post,re.I|re.M|re.S)
        if len1:
            len2 = len(len1.group())
            post = re.sub(r'(?<=(Content-Length: )) *?\d+',str(len2),post,re.I|re.M)
        return post
    
    def cookie(self,post,cookieall):
        global CRLF
        post = post + CRLF
        post = re.sub(r'\r?\n\r?\n\r?\n\r?\n',r'\r\n\r\n',post,re.I|re.M|re.S)
        postdata = post
        for cookie in cookieall.split(','):
            regex = r'Cookie\s{0,5}:.*?$'
            cookies = re.search(regex,postdata,re.I|re.M)
            if cookies:
                cookie1 = cookie.split('=',1)
                regex1 = cookie1[0]+r'='
                cookies1 =re.search(regex1,cookies.group(),re.I|re.M)
                if cookies1:
                    regex2 = cookie1[0]+r'=.*?((?=;)|(?=\s)|(?=&))'
                    postdata = re.sub(regex2,cookie,postdata,re.I|re.M)
                else:
                    regex2 = r'Cookie\s{0,5}:\s*'
                    replace2 = r'Cookie: '+cookie+'; '
                    postdata = re.sub(regex2,replace2,postdata,re.I|re.M)
                print postdata
            else:
                regex1 = r'(Host\s{0,5}:\s*.*)'
                replace1 = r'\1\r\nCookie: '+cookie
                postdata = re.sub(regex1,replace1,postdata,re.I|re.M)
        return postdata
    def domain(self,post,domain):
        regex1 = r'^[Hh]ost\s*?:.*$'
        match = re.search(regex1,post,re.M)
        if not match:
            print colored("\nHost header not found in http request file.",'white','on_red')
            print colored("\nExiting...",'red')
            sys.exit(0)
        a = match.group()
        b = a.split(':')[1].lstrip()
        if b.find(domain) >=0:
            return True
        else:
            return False
		