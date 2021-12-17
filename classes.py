from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.fields.choices import RadioField


class CreateEntry(FlaskForm):
    age = IntegerField('Age')
    sex = StringField('Sex')
    chestPain = StringField('Chest Pain Type')
    restingBP = IntegerField('Resting BP')
    cholestrol = IntegerField('Cholesterol')
    maxHeartRate = IntegerField('Max Heart Rate')
    restingECG = RadioField('Resting ECG?', choices=['Normal', 'LVH', 'ST'])
    exerciseAngina = IntegerField('Exercise Angina')
    heartDisease = IntegerField('Heart Disease? (0 / 1)')
    create = SubmitField('Create')


class DeleteEntry(FlaskForm):
    key = StringField('ID')
    delete = SubmitField('Delete')


class UpdateEntry(FlaskForm):
    key = StringField('ID')
    age = IntegerField('Age')
    sex = StringField('Sex')
    chestPain = StringField('Chest Pain Type')
    restingBP = IntegerField('Resting BP')
    cholestrol = IntegerField('Cholesterol')
    maxHeartRate = IntegerField('Max Heart Rate')
    restingECG = RadioField('Resting ECG?', choices=['Normal', 'LVH', 'ST'])
    exerciseAngina = IntegerField('Exercise Angina')
    heartDisease = IntegerField('Heart Disease? (0 / 1)')
    update = SubmitField('Update')
