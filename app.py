from flask import Flask, render_template, request
from database.db_query import search_email
from database.db_setup import init_db
from logger.custom_logger import log_event
from ml_model.predict import predict_leak
import os

app = Flask(__name__)
   
init_db()
   
@app.route('/')
def index():
    return render_template('index.html')
   
@app.route('/result', methods=['POST'])
def result():
    email = request.form['email']
    log_event(f"Search requested for email: {email}")
    results = search_email(email)
    
    # Create a combined text sample (could be improved later)
    if results:
        combined_text = " ".join([f"{r[0]}: {r[1]} Source: {r[2]}" for r in results])
    else:
        combined_text = f"User queried: {email}"  # fallback

    predicted_label, confidence = predict_leak(combined_text)

    return render_template(
        'result.html',
        email=email,
        results=results,
        predicted_label="Likely Leaked" if predicted_label else "No Leak Detected",
        confidence=confidence
    )
   
if __name__ == '__main__':
    app.run(debug=True)
