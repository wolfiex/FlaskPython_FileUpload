from secure_db import *
import sys


'''
Usage:
python add_user.py name userid passkey
'''
args = sys.argv
sqlc = Database(db_loc,app_key)
print('added: ',args[1], args[2].replace(' ','_'), args[3])
sqlc.add_user( args[1], args[2].replace(' ','_'), args[3])