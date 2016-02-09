import ssl,urllib2
from r_p import f_p
from StringIO import StringIO
import gzip
import zlib
import socket
import os,inspect
import sys
from termcolor import colored
import colorama
from o_n import onh

colorama.init()
options = onh()
if not options.followred:
    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
        def http_error_302(self, req, fp, code, msg, headers):
            pass
        http_error_301 = http_error_303 = http_error_307 = http_error_302
    opener = urllib2.build_opener(MyHTTPRedirectHandler)
    urllib2.install_opener(opener) 

class rqs:
    global file_parsing
    file_parsing = f_p()
    global path
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    def ch_en(self,response):
        if response.info().get('Content-Encoding') == 'gzip' or response.info().get('Content-Encoding') == 'x-gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        elif response.info().get('Content-Encoding') == 'deflate':
            f = StringIO.StringIO(zlib.decompress(response.read()))
            data = f.read()
        else:
            data = response.read()
        return data
    def send_req(self,postdata,ssla,tm,ref,mode,log):
        if ssla == True or mode.lower() =='https':
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            header,body,method,url = file_parsing.f_par(postdata,'Https')
            if method.upper() == 'GET':
                req = urllib2.Request(url,headers=header)
                try:
                    response = urllib2.urlopen(req, context=ctx,timeout=tm)
                except socket.timeout, e:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("The connection has timed out.",'white','on_red')
                    print "Please check the network connectivity or increase the connection timeout using option --contimeout.\n"
                    print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
                    sys.exit(0)
                except urllib2.HTTPError, response:
                    pass
                except urllib2.URLError,response:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("Error occured. Error Message:",'white','on_red')
                    print colored(response.args[0],'white','on_red')
                    sys.exit(0)
                data = self.ch_en(response)
                return data,response.code,url,response.url
            elif method.upper() == 'POST':
                req = urllib2.Request(url,body,header)
                try:
                    response = urllib2.urlopen(req, context=ctx,timeout=tm)
                except socket.timeout, e:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("The connection has timed out.",'white','on_red')
                    print "Please check the network connectivity or increase the connection timeout using option --contimeout.\n"
                    print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
                    sys.exit(0)
                except urllib2.HTTPError, response:
                    pass
                except urllib2.URLError,response:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("Error occured. Error Message:",'white','on_red')
                    print colored(response.args[0],'white','on_red')
                    sys.exit(0)
                data = self.ch_en(response)
                return data,response.code,url,response.url
            else:
                print colored("Method not supported: %s" %(method),'white','on_red')
                sys.exit(0)
        else:
            header,body,method,url = file_parsing.f_par(postdata,'Http')
            if method.upper() == 'GET':
                req = urllib2.Request(url,headers=header)
                try:
                    response = urllib2.urlopen(req,timeout=tm)
                except socket.timeout, e:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("The connection has timed out.",'white','on_red')
                    print "Please check the network connectivity or increase the connection timeout using option --contimeout.\n"
                    print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
                    sys.exit(0)
                except urllib2.HTTPError, response:
                    pass
                except urllib2.URLError,response:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("Error occured. Error Message:",'white','on_red')
                    print colored(response.args[0],'white','on_red')
                    sys.exit(0)
                data = self.ch_en(response)
                return data,response.code,url,response.url
            elif method.upper() == 'POST':
                req = urllib2.Request(url,body,header)
                try:
                    response = urllib2.urlopen(req,timeout=tm)
                except socket.timeout, e:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("The connection has timed out.",'white','on_red')
                    print "Please check the network connectivity or increase the connection timeout using option --contimeout.\n"
                    print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
                    sys.exit(0)
                except urllib2.HTTPError, response:
                    pass
                except urllib2.URLError,response:
                    print colored("\n---------------------------------------------------------------",'cyan')
                    print colored("Error occured. Error Message:",'white','on_red')
                    print colored(response.args[0],'white','on_red')
                    sys.exit(0)
                data = self.ch_en(response)
                return data,response.code,url,response.url
            else:
                print colored("\nMethod not supported: %s" %(method),'white','on_red')
                sys.exit(0)