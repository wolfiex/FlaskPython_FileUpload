# FlaskUpload_withPWD
A simple flask upload program for multiple files requiring credential

## Install pysqlcypher
#### Mac
```
brew install SQLCipher
pip install pysqlcipher3
```
#### Linux 
```
$ sudo apt install sqlcipher libsqlcipher0 libsqlcipher-dev
$ sudo -H pip3 install pysqlcipher3

$ python3 -c 'import pysqlcipher3; print(pysqlcipher3.__path__)'
['/usr/local/lib/python3.7/dist-packages/pysqlcipher3']
```

For code used in the Medium article, look at :

- app.py
- templates/upload_simple.html
- config_simple.py
- secure_db.py 
- new_user.py


Begin by creating a new database:
```
python secure_db.py --wipe
```
and adding a user 
```
python new_user.py bob ./ my_password
```



Now we have a database, we can run the app with 
```
python app.py
```

and the uploaded files should appear in a directory named `uploads_folder` 