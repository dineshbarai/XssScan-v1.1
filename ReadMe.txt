Command to run the tool: python xssscan.py <options>
Mandatory options: -r or -b

Changes:
1. Scanning requests stored in burplog or burp history is possible.
2. Scanning from burp log or history file can be restricted to requests to particular domain or ip address using option --domain=<domain or ip>.
3. User can provide authenticated cookie using option --cookie="<cookie_param=cookie_value>". This cookie would be used in all requests.
4. Colored outputs.

Documentation for XSSScan v1.1 tool:
1. The tool obeys system proxy settings. Hence it is quite easy to capture the request and response on proxy tools by changing the system proxy and restarting the command prompt.
2. Scanning sites on https  requires Python version >=2.7.9 and < 3.x.x. Update python to 2.7.9 before scanning https sites if it is below the this version.
3. Sites on HTTPS can be scanned using  option --ssl.
4. User should provide a request that needs to be scanned in a file and specify the file name using option -r <request_file name> -b <burplog or burp history file name>.
5. The history file in burp suite should be saved with "Base64 encode requests and responses" option checked while saving(This option is checked by default).
6. Scanning from burp log or history file can be restricted to requests to particular domain or ip address using option --domain=<domain or ip>.
7. User can provide authenticated cookie using option --cookie="<cookie_param=cookie_value>". This cookie would be used in all requests.
--------Request Example:-----------------------------------------------------

GET / HTTP/1.1
Host: 127.0.0.1:80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0)
Accept: text/html,application/xhtml+xml,application/xml;q=0.9;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded

------------------------------------------------------------------------------
8. For help, use option -h or --help
9. The tool tries to match the provided script and it url-decoded value in response by default.
10. If --strip option is provided, the tool additionally matches the url-decoded, character stripped(characters provided using --strip option) payload in response.
11. Additionally, user can provide payloads that should be matched for the corresponding script payload in response.txt on the same line as that of the script payload in script.txt. Example: script payload sent in request at nth line in script.txt would expect response stored at nth line in response.txt
12. The tool performs case insensitive response-payload matching (including response from file response.txt, if provided).
13. User can add their own payload in script.txt file and expected response in response.txt on the same corresponding lines.
14. Multiple comma separate expected responses in response.txt file can be defined for a single script payload. Eg: for script payload "<script>alert(1)</script>" two expected responses can be defined as "%3cscript%3ealert(1)%3c/script%3e,<script>alert(123)</script>".
15. The tool by default:
    Scans all parameters.
    Does not include 'Referer' header for scanning. Referer can be included using --increferer option.
    Skips CSRF parameter for testing if Anti-CSRFtoken parameter is defined using option --csrftoken.
    Does not url encode script payload by default. Script payload can be url encoded using --urlencode option.
    Takes script.txt as default script payload file and response.txt as default expected response file. Custom script payloads and expected response can be defined within these files respectively.
16. Scan results are stored in reflected.txt.
17. To see complete list of options, use -h option.

