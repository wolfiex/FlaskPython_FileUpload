import sys,os,re   
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from config_simple import *

from pysqlcipher3 import dbapi2 as sqlite3
from config import app_key, db_loc


app=Flask(__name__)
app.secret_key = app_key
app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024


# Check that the upload folder exists
if not os.path.isdir(upload_dest):
    os.mkdir(upload_dest)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions
    

## on page load display the upload file
@app.route('/upload')
def upload_form():
    return render_template('upload_simple.html')

## on a POST request of data 
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        ### Auth
        user_code = str(request.form.get('psw'))
        
        # Open database
        conn = sqlite3.connect(db_loc)
        cursor = conn.cursor()
        cursor.execute("PRAGMA key='%s'"%app_key)
        
        # Run sql query
        cursor.execute('select * from upload where uploadcode="%s"'%user_code)
        result = cursor.fetchall() 
        
        # close as we are done with it
        conn.close()

        if len(result)==0: 
            # If we do not get a match, send a message
            flash('Not a valid Code')
            return redirect(request.url)
        

        if 'files[]' not in request.files:
            flash('No files found, try again.')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join( upload_dest, filename))

        flash('Files uploaded')
        return redirect('/upload')


if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:4000/upload')
    app.run(host='127.0.0.1',port=4000,debug=True,threaded=True)