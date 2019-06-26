import requests
import time
import json
import sys
import urllib
import base64

import sqlite3
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

user = 'diano'
password = 'harmydiano'
db = sqlite3.connect('data.db')
cursor = db.cursor()


def urlopen(url, data=None):
    '''Open a URL using the urllib2 opener.'''
    request = urllib.request(url, data)
    base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)
    return response


def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jenkins(id INTEGER PRIMARY KEY, job_name TEXT,
                           job_time TEXT, job_status TEXT)
    ''')
    db.commit()


def insert_table(job_name, job_time, job_status):
    cursor.execute('''INSERT INTO jenkins(job_name, job_time, job_status)
                      VALUES(?,?,?,?)''', (job_name, job_time, job_status))
    db.commit()


def show_jobs():
    cursor.execute('''SELECT job_name, job_time, job_status FROM jenkins''')
    for row in cursor:
        print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
        

jenkins_url = 'http://localhost:8080'
build_url = "http://localhost:8080/job/%s/lastBuild/api/json"


J = Jenkins(jenkins_url, 'diano','harmydiano')
jobs = J.keys()


def jenkins_job_status(jobs):
    for job_name in jobs:
        try:
            url = urlopen(jenkins_url + job_name + "/lastBuild/api/json")
            #url = "http://localhost:8080/job/%s/lastBuild/api/json" % job_name
            while True:
                data = json.load(url)
                #data = requests.get(url).json()
                if data['building']:
                    time.sleep(60)
                else:
                    if data['result'] == "SUCCESS":
                        insert_table(job_name, str(data['timestamp']), data['result'])

                        print("Job is success")
                        return True
                    else:
                        insert_table(job_name, str(data['timestamp']), data['result'])
                        print("Job status failed")
                        return False

        except Exception as e:
            print(str(e))
            return False


if __name__ == "__main__":
    create_table()
    if jenkins_job_status(jobs):
        show_jobs()

        print("success")

    else:
        show_jobs()
        print("failed")

