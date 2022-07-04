import csv
import datetime
import os
from uuid import uuid4

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, storage

from functions.functions import snapToDict

load_dotenv()

cred = credentials.Certificate("AccountKey.json")
default_app = firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv("STG_BKT")
})

db = firestore.client()
tasks = db.collection('tasks')
data = snapToDict(tasks)

# Extracts data for each user
users = {}
for taskID in data:
    task = data[taskID]
    ID = task["userID"]
    userData = users.get(ID, [])
    userData.append({"title": task["title"], "failed": task["failed"], "repeatable": task["repeatable"],
                     "completed": task["completed"],
                     "completion_time": (
                             datetime.datetime.fromisoformat(task["end"]) - datetime.datetime.fromisoformat(
                         task["start"])
                     ).total_seconds()})
    users[ID] = userData


# Creates .csv file for each user and uploads it to firebase storage
for user in users:
    data = users[user]
    data_file = open('data.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)

    csv_writer.writerow(data[0].keys())
    for task in data:
        csv_writer.writerow(task.values())
    data_file.close()

    bucket = storage.bucket()
    blob = bucket.blob(str(user) + ".csv")

    # Create new token
    new_token = uuid4()

    # Create new dictionary with the metadata
    metadata = {"firebaseStorageDownloadTokens": new_token}

    # Set metadata to blob
    blob.metadata = metadata

    # Upload file
    blob.upload_from_filename(filename="data.csv", content_type='application/vnd.ms-excel')

# Deletes file after use
if os.path.exists("data.csv"):
    os.remove("data.csv")
else:
    print("The file does not exist")
