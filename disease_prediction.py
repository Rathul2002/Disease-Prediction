import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB

tr=pd.read_csv("./Datasets/Training.csv")
ts=pd.read_csv("./Datasets/Testing.csv")

l1=tr.columns.tolist()
txt=l1[-1]
l1.remove(txt)
l2=[]
for x in range(0,len(l1)):
    l2.append(0)

disease=ts[txt].values.tolist()
dict1={}
dict={}
for i in range(0,len(ts[txt])):
    dict1[ts[txt][i]]= i

dict[txt]=dict1
ts.replace(dict,inplace=True)
tr.replace(dict,inplace=True)

x_train= tr[l1]
y_train = tr[["prognosis"]]
x_test= ts[l1]
y_test = ts[["prognosis"]]

symptoms=[]
days=0

def input_data(lst, d):
    global symptoms, days
    symptoms = lst
    days = d


def Predict_disease():
    gnb = MultinomialNB()
    gnb=gnb.fit(x_train,np.ravel(y_train))
    y_pred = gnb.predict(x_test)

    psymptoms = symptoms
    for k in range(0,len(l1)):
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1
                
    predict = gnb.predict([l2])
    predicted=predict[0]
    Disease=disease[int(predicted)]
    description=Description(Disease)
    precaution=Precaution(Disease)
    severity= Severity_check(symptoms)
    return Disease,description,precaution,severity

def Description(Disease):
    dr=pd.read_csv("./MasterData/symptom_Description.csv")
    ds=0
    for i in range(0,len(dr)):
        if dr['Disease Name'][i]==Disease:
            ds=i
            break
    return dr['Description'][ds]

def Precaution(Disease):
    pr=pd.read_csv("./MasterData/symptom_precaution.csv")
    ds=0
    for i in range(0,len(pr)):
        if pr['Disease Name'][i]==Disease:
            ds=i
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
    sv=pd.read_csv("./MasterData/Symptom_severity.csv")
    sum=0
    #days=int(input("No of days you are suffering: "))
    for j in symptoms:
        ds=0
        for i in range(0,len(sv)):
            if sv['Sympton'][i]==j:
                ds=i
                break
        sum=sum+sv['Severity'][ds]
    sv_check=''
    if((sum*days)/(len(symptoms))>13):
        sv_check="You should take the consultation from doctor."
    else:
        sv_check="It might not be that bad but you should take precautions."
    return sv_check
