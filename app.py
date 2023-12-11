from flask import *
from flask_cors import CORS
from database_functions import *
import pyrebase


app = Flask(__name__)
CORS(app)


firebase_config = {
    "apiKey": "AIzaSyCslAm25aJkWReYOOXV8YNAGzsCVRLkxeM",
    "authDomain": "thawne-d1541.firebaseapp.com",
    "databaseURL": "https://thawne-d1541-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "thawne-d1541",
    "storageBucket": "thawne-d1541.appspot.com",
    "messagingSenderId": "101144409530",
    "appId": "1:101144409530:web:4f2663a71c5c204b4c5983",
    "measurementId": "G-N2NEVEDM49"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()



@app.route('/',methods=["GET", "POST"])
def home():
    return render_template('index.html')

@app.route('/login',methods = ['POST'])
def login():
    user_id = request.form['uid']
    password = request.form['pass']
    login_check(user_id = user_id,password = password)

@app.route('/verifychatuser',methods = ['GET'])
def verify_user():
    user_id = request.args.get('uid')
    chat_id = request.args.get('cid')
    security_level = request.args.get('seclvl')
    password = request.args.get('pass')
    verify_chat_user(user_id = user_id , chat_id = chat_id , security_level = security_level , password = password)


@app.route('/check_user_access',methods = ['GET'])
def check_user_access():
    user_id = request.args.get('uid')
    chat_id = request.args.get('cid')
    check_user_access(user_id = user_id, chat_id = chat_id)


@app.route('/gettopmessages',methods = ['GET'])
def get_top_messages():
    user_id = request.args.get('uid')
    chat_id = request.args.get('cid')
    security_level = request.args.get('seclvl')
    password = request.args.get('pass')
    message_count = request.args.get('msgc')
    get_top_messages(user_id = user_id,chat_id = chat_id, security_level = security_level, password = password, message_count = message_count)




@app.route('/submitmessage',methods = ['POST'])
def save_message():
    user_id = request.form['uid']
    chat_id = request.form['cid']
    security_level = request.form['seclvl']
    password = request.form['pass']
    message_content = request.form['msgcont']

    save_message(user_id = user_id, chat_id = chat_id,security_level = security_level, password = password, message_content = message_content)


@app.route('/getallchat',methods = ['GET'])
def get_all_chat():
    user_id = request.form['uid']
    get_all_chat(user_id = user_id)

    return 200

@app.route('/augmentuser',methods = ['POST'])
def augment_user():
    user_id = request.form['uid']
    subject_user_id = request.form['subuid']
    keyword = request.form['key']
    augment_user(user_id = user_id, subject_user_id = subject_user_id, keyword = keyword)

    return 200

@app.route('/augmentuserchatpermission',methods = ['POST'])
def augment_user_chat_permission():
    user_id = request.form['uid']
    subject_user_id = request.form['subuid']
    chat_id = request.form['cid']
    keyword = request.form['key']
    status = request.form['status']
    augment_user(user_id = user_id, subject_user_id = subject_user_id,chat_id = chat_id, keyword = keyword,status = status)

    return 200

@app.route('/createchat',methods = ['POST'])
def createChat():
    user_id = request.form['uid']
    chat_id = request.form['cid']
    chat_description = request.form['cds']
    chat_name = request.form['chnm']
    security_level = request.form['seclvl']
    list_of_users = request.form['lou']
    general_read = request.form['grd']
    general_write = request.form['gwr']
    
    status, data = create_chat(user_id=user_id, chat_name=chat_name, chat_description=chat_description, chat_id=chat_id, security_level=security_level, list_of_users=list_of_users,  general_read=True, general_write=True)
    if status:
        data = {
        'user_id': user_id,
        'chat_id': chat_id,
        'chat_description': chat_description,
        'chat_name': chat_name,
        'security_level': security_level,
        'list_of_users': list_of_users,
        'general_read': general_read,
        'general_write': general_write
        }

    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True)