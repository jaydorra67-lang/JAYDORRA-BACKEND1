from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import smtplib
import os
from email.mime.text import MIMEText

app = Flask(_name_)
CORS(app)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
ADMIN_EMAIL = "your-email@gmail.com" # <-- CHANGE THIS TO YOUR EMAIL
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
FILE_URL = "https://your-r2-link.com/Pro_Kit.zip" # <-- UPDATE LATER

def send_order_email(customer_phone, amount):
    msg = MIMEText(f"New Jaydorra Order!\n\nPhone: {customer_phone}\nAmount: {amount}\nDownload Link: {FILE_URL}")
    msg['Subject'] = 'New Jaydorra Order Received'
    msg['From'] = ADMIN_EMAIL
    msg['To'] = ADMIN_EMAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
        server.sendmail(ADMIN_EMAIL, ADMIN_EMAIL, msg.as_string())

@app.route("/send_files", methods=["POST"])
def send_files():
    data = request.json
    phone = data.get("phone")
    amount = data.get("amount")
    
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    message = f"Payment verified! 🎉\n\nDownload your Jaydorra Wedding Pro Kit here:\n{FILE_URL}"
    payload = {"messaging_product":"whatsapp","to":phone,"text":{"body":message}}
    requests.post(url, headers=headers, json=payload)
    
    send_order_email(phone, amount)
    return jsonify({"status":"sent"})
