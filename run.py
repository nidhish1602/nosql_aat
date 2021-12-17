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


# def mongoimport(csv_path):
#     """ Imports a csv file at path csv_name to a mongo collection
#     returns: count of the documents in the new collection
#     """
#     coll = db.heart_data
#     try:
#         data = pd.read_csv(csv_path)

#     except FileNotFoundError:
#         return -1

#     payload = json.loads(data.to_json(orient='records'))
#     coll.delete_many({})
#     coll.insert_many(payload)
#     count = coll.count_documents({})
#     db.settings.update_one({"name":'d_id'},{"$set":{'value': count}})
#     print("settings updated")
#     return count


if db.settings.count_documents({'name': 'd_id'}) <= 0:
    print("d_id Not found, creating....")
    db.settings.insert_one({'name': 'd_id', 'value': 0})

csv_path = "heart.csv"
coll = db.heart_data
try:
    data = pd.read_csv(csv_path)

except FileNotFoundError:
    print("File not found")

payload = json.loads(data.to_json(orient='records'))
coll.delete_many({})
coll.insert_many(payload)
count = coll.count_documents({})
db.settings.update_one({"name":'d_id'},{"$set":{'value': count}})
print("settings updated")


def updateID(value):
    d_id = db.settings.find_one()['value']
    d_id += value
    db.settings.update_one(
        {'name': 'd_id'},
        {'$set':
            {'value': d_id}
         })
    print("settings updated")


def createEntry(form):
    age = form.age.data
    sex = form.sex.data
    chestPain = form.chestPain.data
    restingBP = form.restingBP.data
    cholestrol = form.cholestrol.data
    maxHeartRate = form.maxHeartRate.data
    restingECG = form.restingECG.data
    exerciseAngina = form.exerciseAngina.data
    heartDisease = form.heartDisease.data

    d_id = db.settings.find_one()['value']

    # d_entry = {'id': d_id, 'title': title,
    #         'shortdesc': shortdesc, 'priority': priority}
    d_entry = {'id': d_id,
            'age':age,
            'sex':sex,
            'chestPain':chestPain,
            'restingBP':restingBP,
            'cholestrol':cholestrol,
            'maxHeartRate':maxHeartRate,
            'restingECG':restingECG,
            'exerciseAngina':exerciseAngina,
            'heartDisease':heartDisease}

    db.heart_data.insert_one(d_entry)
    print("inserted heart data")
    updateID(1)
    return redirect('/')


def deleteEntry(form):
    key = form.key.data
    db.heart_data.delete_many({'id': int(key)})

    return redirect('/')


def updateEntry(form):
    key = form.key.data
    age = form.age.data
    sex = form.sex.data
    chestPain = form.chestPain.data
    restingBP = form.restingBP.data
    cholestrol = form.cholestrol.data
    maxHeartRate = form.maxHeartRate.data
    restingECG = form.restingECG.data
    exerciseAngina = form.exerciseAngina.data
    heartDisease = form.heartDisease.data

    db.heart_data.update_one(
        {"id": int(key)},
        {"$set":
            {'age':age,
            'sex':sex,
            'chestPain':chestPain,
            'restingBP':restingBP,
            'cholestrol':cholestrol,
            'maxHeartRate':maxHeartRate,
            'restingECG':restingECG,
            'exerciseAngina':exerciseAngina,
            'heartDisease':heartDisease
            }
         }
    )

    return redirect('/')
    
@app.route('/', methods=['GET', 'POST'])
def main():
    # create form
    # csv_path = "heart.csv"
    # if mongoimport(csv_path) == -1:
    #     print("csv not found!")
    # else:
    cform = CreateEntry(prefix='cform')
    uform = UpdateEntry(prefix='uform')
    dform = DeleteEntry(prefix='dform')

    # response
    if cform.validate_on_submit() and cform.create.data:
        return createEntry(cform)
    if dform.validate_on_submit() and dform.delete.data:
        return deleteEntry(dform)
    if uform.validate_on_submit() and uform.update.data:
        return updateEntry(uform)

    # read all data
    docs = db.heart_data.find().sort('_id',-1).limit(10)  # only the last ten
    data = []
    for i in docs:
        data.append(i)

    return render_template('home.html', cform=cform, dform=dform, uform=uform,
                            data=data)


if __name__ == '__main__':
    app.run(debug=True)
