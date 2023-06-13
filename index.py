from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import json

from bot import send_to_all_users
from bot import bot
from bot import start_bot

import os

from waitress import serve

from threading import Thread

from db import Database

db = Database('db/database.db')

app = Flask(__name__)
staticFolder = os.path.join('static')
app.config['UPLOAD_FOLDER'] = staticFolder

def start_app():
    serve(app, host="92.255.76.28", port=3000, url_scheme='https', threads=4)
    #app.run(host="localhost", port=8000)

@app.route('/', methods=['GET'])
def main():
    if request.method == 'GET':
        comments = db.view_comments()
        return render_template('index.html', comments=comments)

@app.route('/postemail', methods=['POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        num = request.form.get('phone-number')
        sel = request.form.get('input-yacht')

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

# @app.route('/static/pictures/photos/evrika/0.jpg', methods=['GET'])
# def photo():
#     if request.method == 'GET':
#         return send_file('\static\pictures\photos\evrika\0.jpg')

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    if request.method == 'GET':
        return send_file('sitemap.xml')

@app.route('/robots.txt', methods=['GET'])
def robots():
    if request.method == 'GET':
        return send_file('robots.txt')
    
@app.errorhandler(404)
def page_not_found(error):
    return redirect("https://more-yacht.ru/")

if __name__ == "__main__":
    t1 = Thread(target=start_app)
    t2 = Thread(target=start_bot)
    t1.start()
    t2.start()
    t1.join()
    t2.join()