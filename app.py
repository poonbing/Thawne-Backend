from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from authenticate.events import AuthenticateNamespace
from chat.events import ChatNamespace
from operation.events import OperationNamespace
from logs.events import LogsNamespace, DataLayer
from file_scan.events import FileScanNamespace
import smtplib,ssl
import schedule
import time as tm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from multiprocessing import Process
import asyncio




app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

class ReportGeneration:
    def __init__(self, app, datalayer):
        print("Hi")
        with app.app_context():
            print("Entered")
            #hardcoded url
            full_url = "http://127.0.0.1:3500/logs"
            self.html = datalayer.Render_List_Of_Dict_To_Html(datalayer._list_of_dict,full_url=full_url)


            with open('output.html','wb') as file_:
                file_.write(self.html.encode("utf-8"))



    def send_report(self):
        sender_email = "thawnetayping@gmail.com"
        password = "umin gflg kvjd mjxm"
        receiver_email = "Snir.Shalev@gmail.com"
        #receiver_email = "[Snir.Shalev@gmail.com,Lewistay03@gmail.com]"

        subject = 'Look at these logs'
        #body = """
        def attach_file_to_email(email_message,filename):
            with open('output.html','rb') as f:
                file_attachment = MIMEApplication(f.read())
            
            file_attachment.add_header("Content-Disposition",f"attachment;filename = {filename}")


            email_message.attach(file_attachment)


        em = MIMEMultipart()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        #em.set_content(body)
        em.attach(MIMEText(self.html,"html"))
        attach_file_to_email(em,'output.html')


        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(sender_email,password)
            smtp.sendmail(sender_email,receiver_email,em.as_string())

    #schedule.every().minute.do(send_report)
    async def run(self):
        print("start run")
        schedule.every(10).seconds.do(self.send_report)
        while True:
            print("looping")
            schedule.run_pending()
            tm.sleep(1)


socketio.on_namespace(AuthenticateNamespace("/auth"))
socketio.on_namespace(ChatNamespace("/chat"))
socketio.on_namespace(OperationNamespace("/operation"))
socketio.on_namespace(LogsNamespace("/log"))
socketio.on_namespace(FileScanNamespace("/filescan"))
report = ReportGeneration(app, DataLayer("UM77682", "poonbing@root"))


@app.route("/")
def default():
    return render_template("index.html")


@app.route("/ping")
def hello_world():
    return "pong"

username = 'UU26473'
password = 'bobbysnir@root'
app = Flask(__name__)
datalayer = DataLayer(username,password)



#print(datalayer._list_of_dict)
@app.route("/logs")
def table():
    # full_url = request.url_root + url_for('table').lstrip('/')
    full_url = None
    return(datalayer.Render_List_Of_Dict_To_Html(datalayer._list_of_dict,full_url))

if __name__ == "__main__":
    socketio.run(app=app, port=5000, debug=True)
    loop = asyncio.get_event_loop()
    loop.create_task(report.run())
    
