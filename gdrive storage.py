import httplib2 
import pprint 
import os.path 
import tarfile 
from datetime import datetime 
import os 
from apiclient.discovery import build 
from apiclient.http import MediaFileUpload 
from oauth2client.client import flow_from_clientsecrets 
from oauth2client.file import Storage

 
CRED_STORAGE_FILE= '/codes/gdrive/credstore' 
CLIENT_SECRET_FILE='/codes/gdrive/client_secrets.json' 
AUTH_SCOPE='https://www.googleapis.com/auth/drive' 
REDIRECT_URI="urn:ietf:wg:oauth:2.0:oob" # FOR INSTALLED APPLICATION 
FOLDER_ID='0BxapbBkxL4puVmVMQWRJUzkzRlE' 
MIME_TYPE="application/x-tgz" 

DESCRIPTION='TESTINGS BRO' 
DIR='/codes' 
BACKUP_DIR='/codes' 

TITLE=''

def build_tarball():
	file_name=str(datetime.now())
	file_name=file_name[0:16]
	file_name=file_name.replace('.','') #making a good file name with time stamp embedded
	file_name=file_name.replace(' ','')
	global TITLE
	TITLE=file_name+'.tar.gz'
	file_name=BACKUP_DIR+'/'+file_name+'.tar.gz'
	tar = tarfile.open(file_name, 'w:gz')
	tar.add(DIR)
	tar.close()
	return file_name 

def initialize():
	store=Storage(CRED_STORAGE_FILE)
	credentials=store.get()
	
	if credentials==None:
		
		flow = flow_from_clientsecrets(CLIENT_SECRET_FILE,AUTH_SCOPE,redirect_uri=REDIRECT_URI)
		authorize_url = flow.step1_get_authorize_url()
		print 'Go to the following link in your browser: ' + authorize_url
		code = raw_input('Enter verification code: ').strip()
		credentials = flow.step2_exchange(code)
		store.put(credentials)
	
	return credentials
	
def clean_up(file_name):
	os.remove(file_name) 

def upload_file():
	credentials=initialize()
	http = httplib2.Http()
	http = credentials.authorize(http)
	drive_service = build('drive', 'v2', http=http)
	file_name=build_tarball()
	file=insert_file(drive_service,TITLE,DESCRIPTION,FOLDER_ID,MIME_TYPE,file_name)
	clean_up(file_name) 

def insert_file(service,title , description,parent_id, mime_type, filename):
 
	media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
	body = {
	'title': title,
	'description': description,
	'mimeType': mime_type
	}
	# Set the parent folder.
	if parent_id:
		body['parents'] = [{'id': parent_id}]
	try:
		file = service.files().insert(
		body=body,
		media_body=media_body).execute()
    		# Uncomment the following line to print the File ID print 'File ID: 
    		# %s' % file['id']
   		return file
	except errors.HttpError, error:
		print 'An error occured: %s' % error
		return None
	

upload_file()
