from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def test():
    # Test rendering the show.html template with sample data
    return render_template("show.html", 
                       prediction=1,
                       spam_confidence=85.5,
                       not_spam_confidence=14.5,
                       email_content="This is a test email content.")

if __name__ == '__main__':
    app.run(debug=True, port=5050)
