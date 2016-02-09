import sys
from optparse import OptionParser
import os,inspect,re
from termcolor import colored
import colorama

colorama.init()

class onh:
    print colored("\nXSSScan v 1.0: XSS scanning tool by Dinesh Barai.\nHTTPS site scanning needs Python version >= 2.7.9 and < 3.x.x.\nIt is recommended to read ReadMe.txt file before using the tool.\n",'cyan')
    usage = "Usage: %prog [options]\n"
    usage += "Mandatory option: -r or -b"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--request", dest="request", help="Name of the file containing the request. Must be in the same directory as of this script.", action="store",default=None)
    parser.add_option("-b","--burplogfile", dest="burplogfile", help="Import HTTP requests from burp log or saved history(requests base64 encoded) file. Must be in the same directory as of this script.", action="store", default=None)
    parser.add_option("--domain", dest="domain", help='Specify domain or IP to which the scanning should be restricted while parsing burp logs or history. Use it in conjunction with --burplogfile option. E.g: --domain="example.com"', action="store", default=None)
    parser.add_option("--ssl", dest="ssl", help="Specify this option for scanning sites on HTTPS", action="store_true", default=False)
    parser.add_option("-u", "--urlencode", dest="urlencode", help="Url encode the script payload before including in the request", action="store_true", default=False)
    parser.add_option("--followred", dest="followred", help="Specify this option to follow redirections(responses with status code 3XX) and read redirected response. By default follow redirection is disabled.", action="store_true", default=False)
    parser.add_option("-t", "--scanone", dest="scanone", help="Scan a single position (marked by *). Default is scan every parameter within a request.", action="store_true", default=False)
    parser.add_option("--doc", dest="doc", help="Shows Documentation stored in ReadMe.txt", action="store_true", default=False)
    parser.add_option("-i", "--increferer", dest="increferer", help="Includes Referer parameters also for scanning. By default Referer header parameters are not included", action="store_true", default=False)
    parser.add_option("-c", "--csrftoken", dest="csrftoken", help="Parameter name which contains Anti-csrf token. The tool would automatically take Anti-csrf token from response and send it in request. Ensure unused Anti-CSRF token is present in the initial HTTP request.", action="store", default=None)
    parser.add_option("--cookie", dest="cookie", help='Specify authenticated cookie that would be sent in each request. Multiple cookies can be specified separated by comma E.g. --cookie="sessionid=ACDE23,testid=ASDedA"', action="store", default=None)
    parser.add_option("-v","--verbose", dest="verbose", help="Turn on verbosity", action="store_true", default=False)
    parser.add_option("-s", "--skipparam", dest="skipparam", help='Comma separated list of parameter names enclosed in "" which are to be excluded from testing',action="store",default=None)
    parser.add_option("--blacklist", dest="blacklist", help='Specify characters or words(case insensitive) blacklisted by application. Usually application produces error or logs out on use of these chars or words as input. Include the characters within "".\nEg:"$,@,!,alert"', action="store", default=None)
    parser.add_option("-l", "--logout", dest="logout", help="Specify unique string in response that indicates that the application has logged out", action="store", default=None)
    parser.add_option("--logoutcode", dest="logoutcode", help="Specify response code that indicates that the application has logged out", action="store", default=None)
    parser.add_option("--shreflected", dest="shreflected", help="Show Scan results (Reflected payloads and point of reflection)", action="store_true", default=False)
    parser.add_option("--contimeout", dest="contimeout", help="Specify connection timeout for request. Default is 30 secs. Use this if there is significant lag in response",type="int", action="store", default=30)
    parser.add_option("--timedelay", dest="timedelay", help="Time delay in seconds between subsequent requests.",type="int", action="store", default=None)
    parser.add_option("--strip", dest="strip", help='Specify any characters or word(case insensitive) that the application is stripping before reflecting the data in response for provided input. This would help in better matching of reflection points. Provide comma separated value enclosed in "".\nEg:"$,@,!,alert"', action="store", default=None)
    
    (options, args) = parser.parse_args()
    scanone = options.scanone
    increferer = options.increferer
    csrftoken = options.csrftoken
    verbose = options.verbose
    request = options.request
    skipparam = options.skipparam
    ssl = options.ssl
    blacklist = options.blacklist
    urlencode = options.urlencode
    logout = options.logout
    logoutcode = options.logoutcode
    doc = options.doc
    shreflected = options.shreflected
    contimeout = options.contimeout
    timedelay = options.timedelay
    strip = options.strip
    burplogfile = options.burplogfile
    cookie = options.cookie
    domain = options.domain
    followred = options.followred
    if len(sys.argv) <2:
        parser.print_help()
        sys.exit(0)
    if options.doc:
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        doc_file = open(path+'/'+'ReadMe.txt','r')
        print doc_file.read()
        doc_file.close()
        sys.exit(0)
    if options.request == None and options.burplogfile == None:
        print colored("Please specify the request file containing the request or burpsuite log using option --request or --burplogfile respectively.",'white','on_red')
        print "For complete list of options, use option -h or --help"
        sys.exit(0)
    if options.request != None and options.burplogfile != None:
        print colored("Please scecify only one from the following options: --request or --burplogfile",'white','on_red')
        sys.exit(0)