from flask import Flask,render_template,request
import pickle

app = Flask(__name__)

pipe = pickle.load(open("Naive_model.pkl","rb"))

@app.route('/', methods=["GET","POST"])
def main_function():
    if request.method == "POST":
        text = request.form
        # print(text)
        emails = text['email']
        print(emails)
        
        list_email = [emails]
        # print(list_email)
        output = pipe.predict(list_email)[0]
        print(output)
        
        # Calculate confidence score
        try:
            proba = pipe.predict_proba(list_email)[0]
            confidence_spam = round(proba[1] * 100, 2)      # Probability of spam
            confidence_not_spam = round(proba[0] * 100, 2)  # Probability of not spam
        except Exception as e:
            confidence_spam = 0
            confidence_not_spam = 0
        
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
                       confidence_spam=confidence_spam,
                       confidence_not_spam=confidence_not_spam,
                       email_text=emails)
    
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)