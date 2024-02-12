import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import uuid
import threading

class ReportGeneration:
    def __init__(self, app, datalayer):
        print("Hi")
        with app.app_context():
            print("Entered")
            random_byte = str(uuid.uuid4().int)[:6]
            print(random_byte)
            full_url = "https://thawne-backend-7skvo7hmpa-uc.a.run.app/log_generation/" + random_byte
            print(full_url)
            self.html = datalayer.Render_List_Of_Dict_To_Html(datalayer._list_of_dict,full_url=full_url)
            with open('output.html','wb') as file_:
                file_.write(self.html.encode("utf-8"))
        self.send_report()


    def send_report(self):
        sender_email = "thawnetayping@gmail.com"
        password = "umin gflg kvjd mjxm"
        receiver_email = "Snir.Shalev@gmail.com"
        subject = 'Look at these logs'
        def attach_file_to_email(email_message,filename):
            with open('output.html','rb') as f:
                file_attachment = MIMEApplication(f.read())
            file_attachment.add_header("Content-Disposition",f"attachment;filename = {filename}")
            email_message.attach(file_attachment)
        em = MIMEMultipart()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.attach(MIMEText(self.html,"html"))
        attach_file_to_email(em,'output.html')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(sender_email,password)
            smtp.sendmail(sender_email,receiver_email,em.as_string())
        print("reschedule")
        self.timer_thread = threading.Timer(10.0, self.send_report)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        print("rescheduled")