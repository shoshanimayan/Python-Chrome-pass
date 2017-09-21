import os
import sys
import json
import csv
import argparse
import sqlite3
import win32crypt

#python program meant to show how to extract passwords from browser as well as show use of databases built stored in the browsers

def valPath(): #gets the file path for the chrome information
    if os.name =="nt": # this is a windows system
        path= (os.getenv("localappdata")+'\\Google\\Chrome\\User Data\\Default\\')
        if not(os.path.isdir(path)):
            print('couldnt find chrome path windows!')
            sys.exit(0)
    print('found path on windows!')
    return path

def recover():#complete function that uses all the other parts to recover passwords and return thm to the user as a json and txt file
    parser = argparse.ArgumentParser(description="Retrieve Google Chrome Passwords")
    parser.add_argument("-o", "--output", choices=['json'],help="Output passwords to JSON  format.")
    parser.add_argument("-d", "--dump", help="Dump passwords to stdout. ", action="store_true")

    args = parser.parse_args()
    
    if args.dump:
        for line in SQLextractor():
            print(line)
            print()
        
    if args.output=='json':
        jsonExtract(SQLextractor())
    return   
    
#print(valPath())

def nameget():
    name=input('name you want to give the file')
    if


def jsonExtract( info): # extracts json data to text
    try:
        name =nameget()
        
        with open(name+'.json', 'w') as json_file:
            json.dump({'password_items': info}, json_file)
        print('success')
    except EnvironmentError:
        print("could not write the data")

def SQLextractor():
    info=[]
    path=valPath()
    try:
        connect = sqlite3.connect(path+'Login Data')
        print('connected')
        with connect:
            cursor = connect.cursor()
            rawData = cursor.execute(
                'SELECT action_url, username_value, password_value FROM logins')
            d = rawData.fetchall()# unencrypted data
            for i in d:
                if os.name =='nt':
                    password = win32crypt.CryptUnprotectData(i[2], None, None, None, 0)[1]
                    if password:
                        info.append({'url':i[0],'user':i[1],'password':str(password)})    
    except sqlite3.operationalError as err:
        print(str(e))
    def alphabet(ele):
        return ele['url']
    info =sorted(info, key=alphabet)
    return info
#------------------------------------------
if __name__ == '__main__':
    recover()
