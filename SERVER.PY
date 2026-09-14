from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(_name_)
CORS(app)  # Allow your frontend to call this

# ===== YOUR GMAIL SETTINGS =====
SENDER_EMAIL = "jaydorra67@gmail.com"
EMAIL_PASSWORD = "roqtbsrafkhhxsnp"  # Your Gmail App Password - no spaces
RECEIVER_EMAIL = "jaydorra67@gmail.com"  # Where you want to receive the messages
# =================================

@app.route("/")
def home():
    return "Jaydorra Backend is running ✅"

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    
    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    if not all([name, email,
