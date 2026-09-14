
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ===== READ FROM RENDER ENVIRONMENT VARIABLES =====
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD") 
RECEIVER_EMAIL = "jaydorra67@gmail.com"
# ===================================================

@app.route("/")
def home():
    return "Jaydorra Backend is running ✅"

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")
        
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"New Contact from {name} - Jaydorra Website"
        
        body = f"""
        You have a new message from your website:
        
        Name: {name}
        Email: {email}
        Message: {message}
        """
        
        msg.attach(MIMEText(body, "plain"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return jsonify({"status": "success", "message": "Email sent!"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if _name_ == "_main_":
    app.run()
