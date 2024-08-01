from flask import Flask, request, render_template
import disease_prediction as dp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = [request.form.get('symptom1'), request.form.get('symptom2'), 
                request.form.get('symptom3'), request.form.get('symptom4'), 
                request.form.get('symptom5')]
    days = request.form.get('days')
    
    valid_symptoms=[]
    
    for s in symptoms:
        if s != 'None':
            valid_symptoms.append(s)

    symptoms = valid_symptoms
    
    if not symptoms and not days:
        return render_template('index.html', prediction_text="Please enter symptoms and number of days.")
    elif not symptoms:
        return render_template('index.html', prediction_text="Please enter valid symptoms.")
    elif not days or int(days) <= 0:
        return render_template('index.html', prediction_text="Please enter a valid number of days.")

    days = int(days)

    result = symptoms, days
    d, desc, prec, sev = dp.Disease_prediction(result)

    return render_template('index.html', prediction_text=f"Disease: {d}", description_text=f"Description: {desc}", precaution_text=f"Precaution: {prec}", severity_text=f"Severity: {sev}")

if __name__ == "__main__":
    app.run(debug=True)
