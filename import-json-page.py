import json
import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='Import JSON file into AEM')

parser.add_argument('--path', nargs='?', required=True)
parser.add_argument('--name', nargs='?', required=True)
parser.add_argument('--host', nargs='?', default='http://localhost:4502')
parser.add_argument('--file', nargs='?', required=True)
parser.add_argument('--user', nargs='?', default='admin')
parser.add_argument('--password', nargs='?', default='admin')
parser.add_argument('--cookie', nargs='?',)

try:
    args = parser.parse_args()
except:
    sys.exit()

destPath = args.path
destHost = args.host
fileToImport = args.file
authUser = args.user
authPass = args.password
authCookie = args.cookie
pageName = args.name

try:
    fileJsonSource = open(fileToImport, "r")
    pageJsonSource = json.load(fileJsonSource)
except:
    print("ERROR: problem with file to import ( ${fileToImport})")
    sys.exit()    

if 'jcr:createdBy' in pageJsonSource:
    del(pageJsonSource['jcr:createdBy'])
if 'jcr:content' in pageJsonSource and 'jcr:createdBy' in pageJsonSource['jcr:content']:
    del(pageJsonSource['jcr:content']['jcr:createdBy'])

if 'jcr:content' in pageJsonSource and 'jcr:baseVersion' in pageJsonSource['jcr:content']:
    del(pageJsonSource['jcr:content']['jcr:baseVersion'])

if 'jcr:content' in pageJsonSource and 'jcr:predecessors' in pageJsonSource['jcr:content']:
    del(pageJsonSource['jcr:content']['jcr:predecessors'])

if 'jcr:content' in pageJsonSource and 'jcr:uuid' in pageJsonSource['jcr:content']:
    del(pageJsonSource['jcr:content']['jcr:uuid'])

if 'jcr:content' in pageJsonSource and 'jcr:versionHistory' in pageJsonSource['jcr:content']:
    del(pageJsonSource['jcr:content']['jcr:versionHistory'])

if 'jcr:content' in pageJsonSource and 'jcr:mixinTypes' in pageJsonSource['jcr:content']:
    del(pageJsonSource['jcr:content']['jcr:mixinTypes'])

if 'jcr:content' in pageJsonSource and 'jcr:isCheckedOut' in pageJsonSource['jcr:content']:
    del(pageJsonSource['jcr:content']['jcr:isCheckedOut'])

url = destHost + destPath

postData = {
    ':operation': 'import',
    ':contentType': 'json',
    ':replace': 'true',
    ':replaceProperties': 'true',
#    :contentFile', '@$j',
    ':content': json.dumps(pageJsonSource),
    ':name': pageName
}

jar = requests.cookies.RequestsCookieJar()
if authCookie:
    print ('we have authorization cookie')
    jar.set('login-token',authCookie)
    auth = None
else:
    auth = (authUser, authPass)

r = requests.post(url, data=postData, headers={}, files={}, cookies=jar, verify=False, auth=auth) #  

print (r.text)
