from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import helper

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "Synergy_db"
mysql = MySQL(app)

otp = {}



@app.route('/')
def start():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
        return
    return render_template('html/start.html', message1="", message2="", show_forget=False)

@app.route('/js')
def start_js():
    return render_template('js/start.js')

@app.route('/main_js')
def main_js():
    return render_template('js/main.js')

@app.route('/about')
def about():
    return render_template('html/about_us.html')

@app.route('/api')
def apis():
    return render_template('html/apis.html')

@app.route('/institution/create')
def create_institution():
    return render_template('html/create_institution.html')

@app.route('/js/institution/create')
def create_institution_js():
    return render_template('js/create_institution.js')

@app.route('/header')
def header():
    return render_template('html/header.html')

@app.route('/header.js')
def header_js():
    return render_template('js/header.js')

@app.route('/home')
def home():
    return render_template('html/home.html')

@app.route('/js/home')
def home_js():
    return render_template('js/home.js')

@app.route('/institute')
def institute():
    return render_template('html/institute.html')

@app.route('/js/institute')
def institute_js():
    return render_template('js/institute.js')

@app.route('/load/home')
def loader1():
    return render_template('html/loader1.html')

@app.route('/load/signup')
def loader2():
    return render_template('html/loader2.html')

@app.route('/load/')
def loader3():
    return render_template('html/loader3.html')

@app.route('/load/institution')
def loader4():
    return render_template('html/loader4.html')

@app.route('/js/load/home')
def loader1_js():
    return render_template('js/loader1.js')

@app.route('/js/load/signup')
def loader2_js():
    return render_template('js/loader2.js')

@app.route('/js/load/')
def loader3_js():
    return render_template('js/loader3.js')

@app.route('/js/load/institution')
def loader4_js():
    return render_template('js/loader4.js')

@app.route('/post')
def post():
    return render_template('html/post.html')

@app.route('/js/post')
def post_js():
    return render_template('js/post.js')

@app.route('/profile')
def profile():
    return render_template('html/profile.html')

@app.route('/js/profile')
def profile_js():
    return render_template('js/profile_js.html')

@app.route('/signup')
def signup():
    return render_template('html/signup.html')

@app.route('/js/signup')
def signup_js():
    return render_template('js/signup.js')

@app.route('/tag')
def tag():
    return render_template('html/tag.html')

@app.route('/js/tag')
def tag_js():
    return render_template('js/tag.js')

@app.route('/login', methods = ['POST'])
def login_form():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    if request.method == "POST":
        username = request.form["inp_start1"]
        password = request.form["inp_start2"]
        query = "SELECT id_obj, id_uniq FROM Account WHERE username = %s"
        cur.execute(query, (username,))
        user = cur.fetchall()
        msg = ""
        if user:
            id_obj = user[0]['id_obj']
            id_uniq = user[0]['id_uniq']
            query = "SELECT pass FROM Personal WHERE id_obj = %s AND id_uniq = %s"
            cur.execute(query, (id_obj, id_uniq))
            user = cur.fetchall()
            cur.close()
            if helper.hash_pwd(password)==user[0]['pass']:
                return render_template('html/home.html', curr_user = id_uniq)
            msg = "Invalid Password"
            return render_template('html/start.html', message1=msg, message2 = "", show_forget=False)
        cur.close()
        msg = "Invalid Username"
        return render_template('html/start.html', message1=msg, message2 = "", show_forget=False)
    
@app.route('/login/otp', methods = ['POST'])
def login_otp_form():
        try:
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in start page")
        if request.method == "POST":
            if request.form["submit_button_start"] == "submit_start1":
                email = request.form["email_start"]
                query = "SELECT email_id FROM Account WHERE email_id = %s"
                cur.execute(query, (email,))
                user = cur.fetchall()
                if user:
                    msg = "Enter OTP"
                    global otp
                    otp[email] = helper.gen_otp()
                    print(otp) #instead send mail function
                    cur.close()
                    return render_template("html/start.html", message1="", message2=msg, show_forget=True, otp_email = email)
                msg = "Email not Registered, Please SignUp"
                cur.close()
                return render_template("html/start.html", message1="", message2=msg, show_forget=True)
            elif request.form["submit_button_start"] == "submit_start2":
                email = request.form["email_start"]
                otp_user = request.form["otp_start"]
                if email in otp:
                    if otp_user == otp[email]:
                        query = "SELECT id_uniq FROM Account WHERE email_id = %s"
                        cur.execute(query, (email,))
                        user = cur.fetchall()
                        id_uniq = user[0]['id_uniq']
                        cur.close()
                        return render_template('html/home.html', curr_user = id_uniq)
                    else:
                        msg = "Invalid OTP"
                        cur.close()
                        return render_template("html/start.html", message1 = "", message2 = msg, show_forget = True, otp_email = email)
                else:
                    msg = "There was some error, try again"
                    cur.close()
                    return render_template("html/start.html", message1 = "", message2 = msg, show_forget = True)
            cur.close()
            return render_template("html/start.html", message1 = "", message2 = "", show_forget=False)

def init_db():
    with app.app_context():
        try:
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in init_db")
            return
        with app.open_resource('schema.sql', mode='r') as sql_file:
            cur.execute(sql_file.read())
        cur.close()
        mysql.connection.commit()
        sql_file.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)