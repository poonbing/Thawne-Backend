from flask import render_template
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from logs.utils import retrieve_log_queue
import threading


class DataLayer:
    def __init__(self,username,password):
        self._username = username
        self._password = password

        result = retrieve_log_queue(username,password)
        #print(result)
        ordered_Dict = 0


        final_order_dict = DataLayer.return_Ordered_Dict(result)
        #print(final_order_dict)

        self._list_of_dict = DataLayer.return_record(final_order_dict)
        #print(self._list_of_dict)
    @staticmethod
    def return_Ordered_Dict(input_tuple):
        if isinstance(input_tuple, tuple) and len(input_tuple) == 2:
            ordered_dict = input_tuple[1]
            return ordered_dict
        
    @staticmethod
    def return_Ordered_Dict_Id(input_tuple):
        if isinstance(input_tuple, tuple) and len(input_tuple) == 2:
            ordered_dict_id = input_tuple[1]
            first_key = next(iter(ordered_dict_id.keys()))
            return first_key
    
    @staticmethod
    def return_record(ordered_dict):
            list_of_dictionaries = []
            for record in ordered_dict:
                #print(final_order_dict[record])
                list_of_dictionaries.append(record)
            return list_of_dictionaries
    @staticmethod
    def Render_List_Of_Dict_To_Html(dictlist,full_url):
        colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

        labels = []
        values = []
        result = {}
        for dict in dictlist:
            key = dict['type of offense'] # type of offense, Breach of Security Policy

            if key in result:
                result[key] = result[key] + 1
            else:
                result[key] = 1

        for key in result:
            labels.append(key)
            values.append(result[key])

        # return render_template("Logs.html",list_of_dict = datalayer._list_of_dict)
        dynamic_data = {
            'list_of_dict': dictlist,
            'max': 17000,
            'set': zip(values, labels, colors), 
            'full_url':full_url
        }
        with open("templates/Logs copy.html", "r") as file:
            print("File Found")
            html_template = file.read()
        rendered_html = html_template.format(**dynamic_data)
        return rendered_html

def send_report():
    try:
        # with app.app_context():
            datalayer = DataLayer("UM77682", "poonbing@root")
            print("Entered")
            #hardcoded url
            # full_url = f"https://thawne-backend-7skvo7hmpa-uc.a.run.app/report"
            full_url = "http://127.0.0.1:5000/report"
            html = datalayer.Render_List_Of_Dict_To_Html(datalayer._list_of_dict,full_url=full_url)
            print("Entered")

            with open('output.html','wb') as file_:
                file_.write(html.encode("utf-8"))

            print("Entered")

            sender_email = "thawnetayping@gmail.com"
            password = "umin gflg kvjd mjxm"
            receiver_email = "thawne.owner@gmail.com"
            #receiver_email = "[Snir.Shalev@gmail.com,Lewistay03@gmail.com]"

            subject = 'Look at these logs'
            #body = """

            @staticmethod
            def attach_file_to_email(email_message,filename):
                with open('output.html','rb') as f:
                    file_attachment = MIMEApplication(f.read())
                
                file_attachment.add_header("Content-Disposition",f"attachment;filename = {filename}")


                email_message.attach(file_attachment)
            print("Entered")

            em = MIMEMultipart()
            em['From'] = sender_email
            em['To'] = receiver_email
            em['Subject'] = subject
            #em.set_content(body)
            em.attach(MIMEText(html,"html"))
            attach_file_to_email(em,'output.html')
            print("Entered")

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(sender_email,password)
                smtp.sendmail(sender_email,receiver_email,em.as_string())
                print("Entered")
            print("Email Sent")
    except Exception as e:
        print(e)
        pass
    timer_thread = threading.Timer(10.0, send_report)
    timer_thread.daemon = True
    timer_thread.start()