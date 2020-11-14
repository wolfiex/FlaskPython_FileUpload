import sys,os,re,glob
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from secure_db import *
from config import *


app=Flask(__name__, 
            static_url_path='', # removes path prefix requirement */templates/static
            static_folder='templates/static',# static file location
            template_folder='templates' # template file location
            )
app.secret_key = app_key
app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024
sqlc = Database(db_loc,app_key)

# Check that the upload folder exists
def makedir (dest):
    fullpath = '%s/%s'%(upload_dest,dest)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)

makedir('')# make uploads folder

## on page load display the upload file
@app.route('/upload')
def upload_form():
    flash('Drag files to upload here.')
    return render_template('upload.html')


## on a POST request of data 
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        psw = str(request.form['psw'])
        #str(request.args.get('psw'))
        allfiles = request.files

        if 'files[]' not in allfiles:
            flash('No files found, try again.')
            return redirect(request.url)

        files = allfiles.getlist('files[]')

        for file in files:
            print (file)
            if file.mimetype in extensions:
                filename = secure_filename(file.filename)
                
                check = sqlc.writefile(psw,filename)
                if (check):
                    makedir(check)
                    file.save(os.path.join(upload_dest,check, filename))
                else:
                    print( 'Wrong Credentials! ')
                    flash('Wrong Credentials!') 
                    return redirect('/upload')
            else:
                print('Not allowed', file)
                
        
        flash('File(s) uploaded')
        return redirect('/upload')



## what have I updated? Return a list of updated files
@app.route('/uploaded/<upload_id>', methods=['GET','POST'])
def data_get(upload_id):
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    
    else: # GET request
        print('%s/%s/*'%(upload_dest,sqlc.writefile(upload_id)))
        files = glob.glob('%s/%s/*'%(upload_dest,sqlc.writefile(upload_id)) ) 
        print ('------',upload_id,files)
        return ','.join([i.rsplit('/',1)[1] for i in files])




if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:4000/upload')
    # lets run this on localhost port 4000
    app.run(host='127.0.0.1',port=4000,debug=True,threaded=True)
