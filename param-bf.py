'''
params:
wordlist1, wordlist2
url
data - in care sa fie cei 2 param pt bruteforce
method

'''


import argparse
import re
import os
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(prog = 'parambf.py', description = 'Bruteforce multiple parameters in an URL', epilog = '\nExample:\n\
                        parambf.py -u https://example.com/login.php -x POST -d "username=^PARAM1^&pass=^PARAM2^" -w1 usernames.txt -w2 passwords.txt -fc 403')

parser.add_argument('-u', metavar='URL', help='URL to bruteforce', required=True)
parser.add_argument('-x', metavar='method', help='GET | POST', required=True)
parser.add_argument('-d', metavar='"param1=^PARAM1^&param2=^PARAM2"', help='data to send, be it GET or POST', required=True)
parser.add_argument('-w1', metavar='wordlist1', help='wordlist for param1', required=True)
parser.add_argument('-w2', metavar='wordlist2', help='wordlist for param2', required=True)


retcode = parser.add_mutually_exclusive_group(required=False)
retcode.add_argument('-fc', help='Filter by response code')
retcode.add_argument('-mc', help='Match response code')


retlen = parser.add_mutually_exclusive_group(required=False)
retlen.add_argument('-fl', help='Filter by lenght')
retlen.add_argument('-ml', help='Match lenght')

string = parser.add_mutually_exclusive_group(required=False)
string.add_argument('-fs', help='Filter by string', required=False)
string.add_argument('-ms', help='Match string', required=False)



def url_check(url):
    # be aware this doesnt match http://localhost, you need at least one . in url ro you need to change this
    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    if re.match(url_pattern, url):
        return True
    else:
        print(bcolors.WARNING + url.strip() + ' is invalid, format should be http[s]://example.com[:port]/' + bcolors.ENDC)
        return False

def check_args(args):
    if(not url_check(args.u)):
        return False
    if(args.x != 'POST' and args.x != 'GET'):
        print(bcolors.WARNING + 'Method should be GET or POST!' + bcolors.ENDC)
        return False
    if('=^PARAM1^' not in args.d and '=^PARAM2^' not in args.d):
        print(bcolors.WARNING + 'Parameter missing from data!' + bcolors.ENDC)
        return False
    if(not os.path.exists(args.w1)):
        print(bcolors.WARNING + 'Wordlist1 not found!' + bcolors.ENDC)
        return False
    if(not os.path.exists(args.w2)):
        print(bcolors.WARNING + 'Wordlist2 not found!' + bcolors.ENDC)
        return False
    return True
    

def main():
    args = parser.parse_args()


    if(not check_args(args)):
        print(bcolors.FAIL + 'Aborting' + bcolors.ENDC)
        exit(-1)
#    else:



    target = args.u
    print((bcolors.BOLD + 'Param1\t\tParam2\t\tCode\t\tLen'+bcolors.ENDC).expandtabs(20))
    with open(args.w1, 'r') as f1:
            lines1 = f1.readlines()
            for line1 in lines1:
                line1 = line1.strip()
                with open(args.w2, 'r') as f2:
                    lines2 = f2.readlines()
                    for line2 in lines2:
                        line2 = line2.strip()
                        data = ((args.d).replace('^PARAM1',line1)).replace('^PARAM2^', line2)
                        if (args.x == 'GET'):
                            target = target + '?' + data
                            r = requests.get(target)
                        else:
                            r = requests.post(target, data=data)

                        #retcode filters
                        if(args.fc):
                            fc = (args.fc).split(',')
                            if(str(r.status_code) in fc):
                                break
                            else:
                                print((bcolors.OKGREEN + line1 + '\t\t' + line2 + '\t\t' + str(r.status_code) + '\t\t' + str(len(r.content)) + bcolors.ENDC).expandtabs(20))

                        elif(args.mc):
                            mc = (args.mc).split(',')
                            if(str(r.status_code) in mc):
                                print((bcolors.OKGREEN + line1 + '\t\t' + line2 + '\t\t' + str(r.status_code) + '\t\t' + str(len(r.content)) + bcolors.ENDC).expandtabs(20))
                            else:
                                break
                        
                        # len filters
                        elif(args.fl):
                            fl = (args.fl).split(',')
                            if(str(len(r.content)) in fl):
                                break
                            else:
                                print((bcolors.OKGREEN + line1 + '\t\t' + line2 + '\t\t' + str(r.status_code) + '\t\t' + str(len(r.content)) + bcolors.ENDC).expandtabs(20))

                        elif(args.ml):
                            ml = (args.ml).split(',')
                            if(str(len(r.content)) in ml):
                                print((bcolors.OKGREEN + line1 + '\t\t' + line2 + '\t\t' + str(r.status_code) + '\t\t' + str(len(r.content)) + bcolors.ENDC).expandtabs(20))
                            else:
                                break

                        # string filters
                        elif(args.fs):
                            if(args.fs in r.text):
                                break
                            else:
                                print((bcolors.OKGREEN + line1 + '\t\t' + line2 + '\t\t' + str(r.status_code) + '\t\t' + str(len(r.content)) + bcolors.ENDC).expandtabs(20))
                        elif(args.ms):
                            if(args.ms in r.text):
                               print((bcolors.OKGREEN + line1 + '\t\t' + line2 + '\t\t' + str(r.status_code) + '\t\t' + str(len(r.content)) + bcolors.ENDC).expandtabs(20))
                            else:
                                break
                         
                        else:
                            print((line1 + '\t\t' + line2 + '\t\t' + str(r.status_code) + '\t\t' + str(len(r.content))).expandtabs(20))




main()
