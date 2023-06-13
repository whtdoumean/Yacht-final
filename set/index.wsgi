from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from flask import Flask, request, render_template, send_file
import os
import json

from bot import start_bot
from bot import send_to_all_users

import os

from waitress import serve

from multiprocessing import Process

# sys.path.append('/root/venv/lib/python3.6/site-packages')

app = Flask(__name__)
staticFolder = os.path.join('static')
app.config['UPLOAD_FOLDER'] = staticFolder
    
def send_email(name, num, sel):
    sender = "Sochi.More.Boat@yandex.ru"
    password = os.environ['MAIL_KEY']
    message = f"Имя клиента: {name}\nТелефон: +7 {num}\nВыбор клиента: {sel}"

    msg = MIMEText(message)
    msg["Subject"] = "Новый клиент!"
    msg["From"] = sender 

    server = SMTP_SSL("smtp.yandex.ru: 465")
    server.ehlo()

    try:
        server.login(sender, password)
        server.sendmail(sender, sender, msg.as_string())
        server.quit()
        return "success"

    except Exception as _ex:
        print(_ex)
        server.quit()
        return "error"

def start_app():
    serve(app, host="92.255.76.28", port=80)

@app.route('/', methods=['GET'])
def main():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/postemail', methods=['POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        num = request.form.get('phone-number')
        sel = request.form.get('input-yacht')

        # if send_email(name, num, sel) == "success":
        if send_to_all_users(name, num, sel) == "success":
            response = {"message": "Успешно!"}
        else:
            response = {"message": "Данные не отправлены"}

        json.dumps(response)
        return response

@app.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    if request.method == 'GET':
        return send_file('static/documents/privacy_policy.pdf')

@app.route('/personal_DATA', methods=['GET'])
def personal_DATA():
    if request.method == 'GET':
        return send_file('static/documents/personal_DATA.pdf')

if __name__ == "__main__":
    p1 = Process(target=start_bot)
    p1.start()
    #p2 = Process(target=start_app)
    #p2.start()
    p1.join()
    #p2.join()   
