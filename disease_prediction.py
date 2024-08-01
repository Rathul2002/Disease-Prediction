import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC 
from sklearn.naive_bayes import GaussianNB 
from sklearn.ensemble import RandomForestClassifier 
from statistics import mode
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn.base')
data = pd.read_csv('./Datasets/Training.csv').dropna(axis=1)
encoder= LabelEncoder()
data['prognosis'] = encoder.fit_transform(data["prognosis"])

train_X = data.iloc[:,:-1]
train_Y = data.iloc[:,-1]

test_data=pd.read_csv('./Datasets/Testing.csv')
test_X = test_data.iloc[:, :-1] 
test_Y = encoder.transform(test_data.iloc[:, -1])

input_symptoms = []
input_days = 0
symptoms = train_X.columns.values 
symptom_index = {} 
for index, value in enumerate(symptoms): 
    symptom = " ".join([i.capitalize() for i in value.split("_")]) 
    symptom_index[symptom] = index 
  
data_dict = { 
    "symptom_index":symptom_index, 
    "predictions_classes":encoder.classes_ 
} 


def input_data(lst, d):
    global input_symptoms, input_days
    input_symptoms = lst
    input_days = d
    
def prediction():
    svm_model = SVC() 
    nb_model = GaussianNB() 
    rf_model = RandomForestClassifier(random_state=18) 
    svm_model.fit(train_X, train_Y) 
    nb_model.fit(train_X, train_Y) 
    rf_model.fit(train_X, train_Y)
    
    input_data = [0] * len(data_dict["symptom_index"]) 
    for symptom in input_symptoms: 
        index = data_dict["symptom_index"][symptom] 
        input_data[index] = 1
        
    input_data = np.array(input_data).reshape(1,-1) 
    rf_prediction = data_dict["predictions_classes"][rf_model.predict(input_data)[0]] 
    nb_prediction = data_dict["predictions_classes"][nb_model.predict(input_data)[0]] 
    svm_prediction = data_dict["predictions_classes"][svm_model.predict(input_data)[0]] 
    prediction = mode([rf_prediction, nb_prediction, svm_prediction]) 
    
    return prediction

def Description(Disease):
    dr = pd.read_csv("./MasterData/symptom_Description.csv")
    ds = 0
    for i in range(0, len(dr)):
        if dr['Disease Name'][i] == Disease:
            ds = i
            break
    return dr['Description'][ds]
    
def Precaution(Disease):
    pr = pd.read_csv("./MasterData/symptom_precaution.csv")
    ds = 0
    for i in range(0, len(pr)):
        if pr['Disease Name'][i] == Disease:
            ds = i
            break
    precaution_parts = [
        str(pr['Precaution 1'][ds]),
        str(pr['Precaution 2'][ds]),
        str(pr['Precaution 3'][ds]),
        str(pr['Precaution 4'][ds])
    ]

    precaution = '\n'.join(precaution_parts)
    return precaution

def Severity_check(symptoms):
    sv = pd.read_csv("./MasterData/Symptom_severity.csv")
    add = 0
    for j in symptoms:
        ds = 0
        for i in range(0, len(sv)):
            if sv['Sympton'][i] == j:
                ds = i
                break
        add = add + sv['Severity'][ds]
    sv_check = ''
    if (add * input_days) / (len(symptoms)) > 13:
        sv_check = "You should take the consultation from doctor."
    else:
        sv_check = "It might not be that bad but you should take precautions."
    return sv_check


def Disease_prediction(message):
    symp, time = message
    input_data(symp, time)
    disease = prediction()
    description = Description(disease)
    precaution = Precaution(disease)
    severity=Severity_check(input_symptoms)
    
    return disease,description,precaution,severity
    