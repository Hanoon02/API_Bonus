from mmap import PAGESIZE
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly']


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


# Using credential and user input, we return the course
def getCourseMaterials(creds, id):
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().courseWorkMaterials().list(
        courseId=course_id[id], pageSize=10).execute()
    courses = results.get('courseWorkMaterial')
    nextPage = results.get('nextPageToken')
    return courses


def getNextList(creds, id):
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().courseWorkMaterials().list(
        courseId=course_id[id], pageSize=10, pageToken=nextPage).execute()
    courses = results.get('courseWorkMaterial')
    nextPage = results.get('nextPageToken')
    return nextPage


def getForEach():  # To get courses for each
    course = int(input(
        "Please choose which course material would you like to obtain: \n1. IP\n2. HCI\n3. LA\n4. COM\n5. DC\nEnter your number: "))
    courseMaterial = getCourseMaterials(creds, course)
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


def getAll():
    allfile = []
    for t in range(1, 6):
        courseMaterial = getCourseMaterials(creds, course_id[t])
        try:
            for i in courseMaterial:
                try:
                    print(i['materials'])
                    for j in i['materials']:
                        allfile.append("Material Name: ",
                                       j["driveFile"]["driveFile"]["title"] +
                                       " : "+j["driveFile"]
                                       ["driveFile"]["alternateLink"])
                except:
                    continue
        except:
            continue

    return allfile


# These are my course ID, i believe everyone get their own ID, not sure
course_id = {1: "450521735596", 2: "450438402077",
             3: "450548719985", 4: "450464887023", 5: "451576098760"}
creds = get_cred()
type = int(input(
    "Please choose the method by which you want to retrieve the files: \n1.Get for each course seperately\n2.Get all\nPlease enter the number: "))
if type == 1:
    getForEach()
elif type == 2:
    allfiles = getAll()
    print(allfiles)
