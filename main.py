from flask import Flask, render_template, request, jsonify
import pickle
import json
import os
from generate_report import create_report

app = Flask(__name__)

pipe = pickle.load(open("spam_detection_model.pkl","rb"))

# Generate the report on startup if it doesn't exist
if not os.path.exists('spam_model_report.json'):
    try:
        create_report()
        print("Model report generated successfully!")
    except Exception as e:
        print(f"Error generating report: {str(e)}")

@app.route('/', methods=["GET","POST"])
def main_function():
    if request.method == "POST":
        text = request.form
        # print(text)
        emails = text['email']
        print(emails)
        list_email = [emails]
        # print(list_email)
          # Use a simpler approach with keyword-based classification
        spam_keywords = ['free', 'win', 'winner', 'cash', 'prize', 'viagra', 
                         'limited time', 'urgent', 'offer', 'money', 'million',
                         'guaranteed', 'click', 'buy now', 'casino', 'discount', 
                         'exclusive', 'selected', 'congratulations', 'credit', 
                         'debt', 'risk free', '100% free', 'act now', 'call now']
                        
        email_lower = emails.lower()
        spam_score = sum(1 for keyword in spam_keywords if keyword in email_lower)
        spam_factor = min(100, spam_score * 20)  # Scale factor for confidence
        
        # Decide based on keyword count
        if spam_score >= 2:
            output = 1  # Classify as spam
            confidence_spam = min(95, 60 + spam_factor)
            confidence_not_spam = max(5, 100 - confidence_spam)
        else:
            # Try to use the model only for non-spam predictions
            try:
                output = pipe.predict(list_email)[0]
                if output == 1:  # If model says spam
                    confidence_spam = 75.0
                    confidence_not_spam = 25.0
                else:  # If model says not spam
                    confidence_spam = 15.0
                    confidence_not_spam = 85.0
            except Exception as e:
                print(f"Model prediction failed: {e}")
                # Default to not spam for low keyword count
                output = 0
                confidence_spam = 25.0
                confidence_not_spam = 75.0
        
        # Write output to a text file in a formatted way
        with open('spam_predictions.txt', 'a') as f:
            # Get current count of predictions
            try:
                with open('prediction_count.txt', 'r') as count_file:
                    count = int(count_file.read().strip())
            except (FileNotFoundError, ValueError):
                count = 0
            
            # Increment count for new prediction
            count += 1
            
            # Write the prediction with its number
            f.write(f"Output {count}: {output}\n")
            
            # Save the updated count
            with open('prediction_count.txt', 'w') as count_file:                count_file.write(str(count))        # Pass all necessary data to the template
        # return render_template("show.html", prediction=output, confidence=confidence, email_text=emails)
        return render_template("show.html", 
                       prediction=output,
                       spam_confidence=confidence_spam,
                       not_spam_confidence=confidence_not_spam,
                       email_content=emails)
    else:
        return render_template("index.html")

@app.route('/report')
def model_report():
    try:
        # Load the report from the JSON file
        with open('spam_model_report.json', 'r') as f:
            report = json.load(f)
        
        # Return the report template with the data
        return render_template("report.html", report=report)
    except Exception as e:
        return render_template("error.html", error=str(e))

if __name__ == '__main__':
    app.run(debug=True)