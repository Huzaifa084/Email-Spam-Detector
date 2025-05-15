from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the model
try:
    pipe = pickle.load(open("Naive_model.pkl","rb"))
except:
    print("Error loading model. Make sure Naive_model.pkl exists.")

# Add confidence score to predictions
@app.route('/', methods=["GET","POST"])
def main_function():
    if request.method == "POST":
        email_text = request.form['email']
        
        # Input validation
        if not email_text or len(email_text) < 5:
            return render_template("show.html", prediction="Invalid Input", 
                                  confidence=0, email_text=email_text)
        
        # Get prediction
        list_email = [email_text]
        output = pipe.predict(list_email)[0]
        
        # Get probability scores for more information
        try:
            proba = pipe.predict_proba(list_email)[0]
            confidence = round(proba[output] * 100, 2)
        except:
            confidence = "N/A"
            
        return render_template("show.html", prediction=output, 
                              confidence=confidence, email_text=email_text)
    
    return render_template("index.html")

# Add API endpoint
@app.route('/api/predict', methods=["POST"])
def predict_api():
    data = request.json
    if not data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400
        
    prediction = pipe.predict([data['email']])[0]
    return jsonify({"prediction": int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)