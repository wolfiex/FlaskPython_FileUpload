import os 
'''
Global arguments
'''
# maximum filesize in megabytes
file_mb_max = 100
# encryption key
app_key = 'test'
# full path destination for our upload files
upload_dest = os.path.join(os.getcwd(), 'uploads_folder')
# list of allowed allowed extensions
extensions = set(['txt', 'pdf', 'image/png', 'image/tiff','image/gtiff'])
#text/html 
db_loc = os.path.join(os.getcwd(), 'user_cred.db')
