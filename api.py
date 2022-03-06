import os.path
import os
import io
import json
from urllib import response
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
          'https://www.googleapis.com/auth/classroom.courses.readonly']


def get_cred():  # To get the credential
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def classCodes(creds=get_cred()):
    courseDetails = {}
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    for course in courses:
        courseDetails[course['name']] = course['id']
    return courseDetails


# Using credential and user input, we return the course
def getCourseMaterials(creds, id):
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().courseWorkMaterials().list(
        courseId=course_id[id], pageSize=10).execute()
    courses = results.get('courseWorkMaterial')
    return courses


def viewMaterials():  # To get courses for each
    names = list(course_id.keys())
    course = int(input(
        f"Please choose which course material would you like to obtain: \n1. {names[0]}\n2. {names[1]}\n3. {names[2]}\n4. {names[3]}\n5. {names[4]}\nEnter your number: "))
    courseMaterial = getCourseMaterials(creds, names[course-1])
    try:
        for i in courseMaterial:
            try:
                print("----------------------------------------------------------------------------------------------------------------")
                print("Title: ", i['title'])
                for j in i['materials']:
                    print("Material Name: ",
                          j["driveFile"]["driveFile"]["title"])
                    print("Link: ", j["driveFile"]
                          ["driveFile"]["alternateLink"])
                    print()
                print()
            except:
                print("----------------------------------------------------------------------------------------------------------------")
                print("File could not be retrieved")
    except:
        print("The course contains no materials")
    pass


def downloadMaterial():
    names = list(course_id.keys())
    course = int(input(
        f"Please choose which course material would you like to obtain: \n1. {names[0]}\n2. {names[1]}\n3. {names[2]}\n4. {names[3]}\n5. {names[4]}\nEnter your number: "))
    courseMaterial = getCourseMaterials(creds, names[course-1])
    k = 1
    with open("DriveLinks.txt", "w")as q:
        try:
            for i in courseMaterial:
                try:
                    print(
                        "----------------------------------------------------------------------------------------------------------------")
                    print("Title: ", i['title'])
                    for j in i['materials']:
                        print(f"{k}. Material Name: ",
                              j["driveFile"]["driveFile"]["title"])
                        q.write(
                            f"{j['driveFile']['driveFile']['alternateLink']}\n")
                        k += 1
                except:
                    pass
        except:
            pass
    files = list(
        map(int, input("Please enter the files you want to download: ").split()))
    with open("DriveLinks.txt", "r")as t:
        with open("DownloadLinks.txt", "w") as d:
            for file in files:
                d.write(f"{t.readlines()[file-1]}")
                t.seek(0)
    pass


def getClassCodes():
    if os.path.isfile('className.txt'):
        with open('className.txt', 'r') as f:
            data = json.load(f)
        return data
    else:
        with open('className.txt', 'w') as f:
            data = classCodes()
            print(data)
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data


course_id = getClassCodes()
creds = get_cred()
type = int(input(
    "Please choose the method by which you want to retrieve the files: \n1.View course materials directly\n2.Download course materials materials\nPlease enter the number: "))
if type == 1:
    viewMaterials()
elif type == 2:
    downloadMaterial()
