from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345678"
app.config["MYSQL_DB"] = "Synergy_db"
mysql = MySQL(app)



@app.route('/')
def start():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    return render_template('html/start.html')

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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    if request.method == "POST":
        userid = request.form.get('userid')
        password = request.form.get('user_password')
        # cursor.exec
        # cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE name = %s", (userid,))
        # mysql.connection.commit()
        # report=cursor.fetchall()
        # print(report)
        # return "Report: " + report
        user = cur.fetchall()
        cur.close()
        if user:
            # print("oks ", type(user))
            # print(user[0]['id'])
            # if(type(user) == tuple):
            #     print("hi")
            #     render_template("./signup.html")
            # return render_template('searchResult.html', results=user[0])
            if user[0]['password'] != password:
                return render_template('searchResult.html', results="Incorrect Password")
            return render_template('./home.html', results="Not a valid username")
        return render_template('searchResult.html', results="Not a valid username")
    return render_template("./signup.html")

def init_db():
    with app.app_context():
        try:
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in init_db")
        with app.open_resource('schema.sql', mode='r') as sql_file:
            cur.execute(sql_file.read())
        cur.close()
        mysql.connection.commit()
        sql_file.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)