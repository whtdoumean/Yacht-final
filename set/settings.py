import os

def creating_keys():
    with open('.env', 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            os.environ[line[:line.find("=")]] = line[line.find("=") + 1:]

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
