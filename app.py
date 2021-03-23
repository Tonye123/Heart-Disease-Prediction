# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 16:06:19 2021

@author: Tonye
"""
from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

with open('classifier_mod2.pkl', 'rb') as pickle_file:
    model = pickle.load(pickle_file)


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


@app.route('/Predict', methods=['POST'])
def Predict():
    if request.method == 'POST':
        sex = request.form['sex']
        if(sex == 'male'):
            sex = 1
        else:
            sex = 0
        Ca = int(request.form['colored vessels'])
        ChestPain = request.form['chest']
        if(ChestPain == 'asym'):
            ChestPain_asymptomatic = 1
            ChestPain_nona = 0
            ChestPain_atyp = 0
            ChestPain_typ = 0
        elif(ChestPain == 'nona'):
            ChestPain_asymptomatic = 0
            ChestPain_nona = 1
            ChestPain_atyp = 0
            ChestPain_typ = 0
        elif(ChestPain == 'typ'):
            ChestPain_asymptomatic = 0
            ChestPain_nona = 0
            ChestPain_atyp = 0
            ChestPain_typ = 1
        else:
            ChestPain_asymptomatic = 0
            ChestPain_nona = 0
            ChestPain_atyp = 1
            ChestPain_typ = 0

        Thal = request.form['thal']
        if(Thal == 'norm'):
            Thal_normal = 1
            Thal_fixed = 0
            Thal_reversable = 0
        elif(Thal == 'fixed'):
            Thal_normal = 0
            Thal_fixed = 1
            Thal_reversable = 0
        else:
            Thal_normal = 0
            Thal_fixed = 0
            Thal_reversable = 1

        Fbs = request.form['fbs']
        if(Fbs == 'yes'):
            Fbs = 1
        else:
            Fbs = 0
        Age = int(request.form['age'])
        Oldpeak = float(request.form['peak'])
        MaxHR = int(request.form['hr'])
        Chol = int(request.form['chol'])
        Ex_Ang = request.form['ExAng']
        if(Ex_Ang == 'yes'):
            Ex_Ang = 1
        else:
            Ex_Ang = 0
        RestBP = int(request.form['bp'])
        RestECG = int(request.form['ecg'])
        Slope = request.form['slope']
        if(Slope == 'up'):
            Slope = 1
        elif(Slope == 'flat'):
            Slope = 2
        else:
            Slope = 3

        prediction = model.predict([[Age, sex, RestBP, Chol, Fbs, RestECG, MaxHR, Ex_Ang, Oldpeak, Slope, Ca,
                                   ChestPain_asymptomatic, ChestPain_nona, ChestPain_atyp, ChestPain_typ, Thal_fixed, Thal_normal, Thal_reversable]])
        if prediction[0] == 1:
            return render_template('result.html', prediction_text="Yes - You are prone to Heart Disease")
        else:
            return render_template('result.html', prediction_text="No - You are not prone to Heart Disease")

    else:
        render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
