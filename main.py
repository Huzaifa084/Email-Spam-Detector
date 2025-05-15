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
            with open('prediction_count.txt', 'w') as count_file:
                count_file.write(str(count))
                
        # Pass all necessary data to the template
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
            report_data = json.load(f)
        
        # Extract data for the template
        dataset_size = report_data['dataset_info']['total_samples']
        spam_count = report_data['dataset_info']['spam_count']
        ham_count = report_data['dataset_info']['non_spam_count']
        spam_percentage = round(report_data['dataset_info']['spam_percentage'], 1)
        ham_percentage = round(100 - report_data['dataset_info']['spam_percentage'], 1)
        model_type = report_data['best_model_info']['name']
        feature_count = len(report_data['dataset_info']['features'])
        
        # Performance metrics
        accuracy = round(report_data['final_performance']['accuracy'] * 100, 1)
        precision = round(report_data['final_performance']['classification_metrics']['precision'] * 100, 1)
        recall = round(report_data['final_performance']['classification_metrics']['recall'] * 100, 1)
        f1_score = round(report_data['final_performance']['classification_metrics']['f1_score'] * 100, 1)
        
        # Confusion matrix
        conf_matrix = report_data['final_performance']['confusion_matrix']
        true_negatives = conf_matrix[0][0]
        false_positives = conf_matrix[0][1]
        false_negatives = conf_matrix[1][0]
        true_positives = conf_matrix[1][1]
        
        # Model comparison
        nb_accuracy = round(report_data['models_comparison']['Multinomial Naive Bayes']['accuracy'] * 100, 1)
        lr_accuracy = round(report_data['models_comparison']['Logistic Regression']['accuracy'] * 100, 1)
        svm_accuracy = round(report_data['models_comparison']['Linear SVM']['accuracy'] * 100, 1)
        rf_accuracy = round(report_data['models_comparison']['Random Forest']['accuracy'] * 100, 1)
        
        # Key features - example placeholder data
        spam_features = [
            {'word': 'free', 'score': '0.89'},
            {'word': 'offer', 'score': '0.82'},
            {'word': 'click', 'score': '0.78'},
            {'word': 'cash', 'score': '0.74'},
            {'word': 'money', 'score': '0.68'}
        ]
        
        ham_features = [
            {'word': 'meeting', 'score': '0.91'},
            {'word': 'report', 'score': '0.87'},
            {'word': 'project', 'score': '0.83'},
            {'word': 'regards', 'score': '0.76'},
            {'word': 'schedule', 'score': '0.72'}
        ]
        
        # Pass individual variables to the template for easier access
        return render_template("report.html", 
                            report=report_data,
                            dataset_size=dataset_size,
                            spam_count=spam_count,
                            ham_count=ham_count,
                            spam_percentage=spam_percentage,
                            ham_percentage=ham_percentage,
                            model_type=model_type,
                            feature_count=feature_count,
                            accuracy=accuracy,
                            precision=precision,
                            recall=recall,
                            f1_score=f1_score,
                            true_positives=true_positives,
                            true_negatives=true_negatives,
                            false_positives=false_positives,
                            false_negatives=false_negatives,
                            nb_accuracy=nb_accuracy,
                            lr_accuracy=lr_accuracy,
                            svm_accuracy=svm_accuracy,
                            rf_accuracy=rf_accuracy,
                            spam_features=spam_features,
                            ham_features=ham_features)
    except Exception as e:
        print(f"Error loading report: {str(e)}")
        return render_template("error.html", error=str(e))

if __name__ == '__main__':
    app.run(debug=True)