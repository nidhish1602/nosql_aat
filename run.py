from flask import Flask, render_template, redirect
from pymongo import MongoClient
from classes import *
import pandas as pd
import json

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient('localhost:27017')
db = client.HeartFailure


def mongoimport(csv_path):
    """ Imports a csv file at path csv_name to a mongo collection
    returns: count of the documents in the new collection
    """
    coll = db.heart_data
    try:
        data = pd.read_csv(csv_path)

    except FileNotFoundError:
        return -1

    payload = json.loads(data.to_json(orient='records'))
    coll.delete_many({})
    coll.insert_many(payload)
    return coll.count()


if db.settings.count_documents({'name': 'd_id'}) <= 0:
    print("d_id Not found, creating....")
    db.settings.insert_one({'name': 'd_id', 'value': 0})


def updateID(value):
    d_id = db.settings.find_one()['value']
    d_id += value
    db.settings.update_one(
        {'name': 'd_id'},
        {'$set':
            {'value': d_id}
         })


def createDocument(form):
    title = form.title.data

    d_id = db.settings.find_one()['value']

    # d_entry = {'id': d_id, 'title': title,
    #         'shortdesc': shortdesc, 'priority': priority}

    d_entry = {'id': d_id}

    db.heart_data.insert_one(d_entry)
    updateID(1)
    return redirect('/')


def deleteDocument(form):
    key = form.key.data
    db.heart_data.delete_many({'id': int(key)})

    return redirect('/')


def updateDocument(form):
    key = form.key.data
    age = form.age.data

    db.heart_data.update_one(
        {"id": int(key)},
        {"$set":
            {"age": age}
         }
    )

    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def main():
    # create form
    csv_path = "heart.csv"
    if mongoimport(csv_path) == -1:
        print("csv not found!")
    else:
        cform = CreateEntry(prefix='cform')
        uform = UpdateEntry(prefix='uform')
        dform = DeleteEntry(prefix='dform')

        # response
        if cform.validate_on_submit() and cform.create.data:
            return createDocument(cform)
        if dform.validate_on_submit() and dform.delete.data:
            return deleteDocument(dform)
        if uform.validate_on_submit() and uform.update.data:
            return updateDocument(uform)

        # read all data
        docs = db.heart_data.find().limit(5)  # only the first five
        data = []
        for i in docs:
            data.append(i)

        return render_template('home.html', cform=cform, dform=dform, uform=uform,
                               data=data)


if __name__ == '__main__':
    app.run(debug=True)
