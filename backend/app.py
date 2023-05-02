
from flask import Flask, render_template, request, url_for, redirect, session, jsonify, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import helper
from datetime import datetime
from dateutil.relativedelta import relativedelta
import io
from io import BytesIO
import zipfile
import requests
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user, login_manager
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from PIL import Image, ImageDraw, ImageFont
import random
import io
from flask import g, request, redirect, url_for
from flask_login import current_user
from functools import wraps

# Function to generate a random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to generate an image with a solid color and a text label
def generate_image():
    # Create a new image with a solid color\
    img = Image.new('RGB', (100, 100), color=random_color())
    # Draw a text label on the image
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    label = '  No Profile \n    Photo'
    draw.text((10, 40), label, font=font, fill=(255, 255, 255))
    # Save the image to a buffer
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    # Return the image contents
    return buf.getvalue()

app = Flask(__name__)
app.secret_key = "devang"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id) -> None:
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('start'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    g.user = current_user

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "Synergy_db"
mysql = MySQL(app)

otp = {}
otp_signup = {}
otp_institute = {}
feed = []
comment_list = []
post_ = []
profile_data = []
stats = []
my_post = []
institute_data = []
inst_post = []

db = MySQLdb.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'], password=app.config['MYSQL_PASSWORD'], db=app.config['MYSQL_DB'])

@app.route('/logout')
@login_required
def logout():
    if session['user']:
        logout_user()
        global otp
        global otp_signup
        global otp_institute
        global feed
        global comment_list
        global post_
        global profile_data
        global stats
        global my_post 
        global institute_data 
        global inst_post
        otp = {}
        otp_signup = {}
        otp_institute = {}
        feed = []
        comment_list = []
        post_ = []
        profile_data = []
        stats = []
        my_post = []
        institute_data = []
        inst_post = []
        session['user'] = {}
    return render_template('html/start.html')

@app.route('/')
def start():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
        return
    return render_template('html/start.html', message1="", message2="", show_forget=False)

@app.route('/post/upvote', methods = ['POST'])
@login_required
def upvote_for_post():
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        post_id = request.form.keys()
        post_id = list(post_id)[0]
        temp_ind = post_id.index("-")
        post_num = int(post_id[temp_ind+1:])
        if feed[post_num][2]:
            helper.downvote_for_post_help(cur, session['user']['id_uniq'], feed[post_num][0])
        else:
            helper.upvote_for_post_help(cur, session['user']['id_uniq'], feed[post_num][0])
        mysql.connection.commit()
        cur.close()
    
    return redirect("/home")


@app.route('/home/follow', methods = ['POST']) # how to show the account name here ??
@login_required
def follow_account():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    key_id = request.form.keys()
    key_id = list(key_id)[0]
    temp_ind = key_id.index("-")
    post_num = int(key_id[temp_ind+1:])
    sender_id = session['user']['id_uniq']
    profile_username = feed[post_num][4]
    query = "SELECT id_uniq from Account WHERE username = '{}'".format(profile_username)
    cur.execute(query)
    receiver_id = cur.fetchall()[0]['id_uniq']
    if feed[post_num][8]:
        helper.unfollow_help(cur, sender_id, receiver_id)
    else:
        helper.follow_help(cur, sender_id, receiver_id)
    mysql.connection.commit()
    cur.close()
    return redirect("/home")


@app.route('/home/post', methods = ['POST'])
@login_required
def post_input():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        postTitle = request.form['posttit']
        postTags = request.form['posttags']
        postTags = postTags.split(";")
        postTags = [x.strip() for x in postTags]
        postDescription = request.form['post_description']
        postDescription = postDescription.replace("\n","<br>")
        postTitle = postTitle.replace("'","&apos;")
        postDescription = postDescription.replace("'","&apos;")
        Tags = []
        for x in postTags:
            x = x.replace("'","&apos;")
            if x != "":
                Tags.append(x)
        postTags = Tags
        postInst = request.form['postinst']
        postInst = postInst.split(";")
        postInst = [x.strip() for x in postInst]
        institute = []
        for x in postInst:
            x = x.replace("'","&apos;")
            if x != "":
                institute.append(x)
        postInst = institute
        author_id = session['user']['id_uniq']
        post_id = helper.id_gen(cur, 'P', session['user']['username'], 'Post')
        query = "INSERT INTO Post (id_obj, id_uniq, author_obj, author_uniq, title, content, upvotes, comments, report_list, public_post, visibility,  institutes, tag_list, api_visibility) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', '{}', {});".format('P', post_id[1:], 'A', author_id, postTitle, postDescription, post_id[1:]+'_upv', post_id[1:]+'_com', post_id[1:]+'_rep', True, True, post_id[1:]+'_ins', post_id[1:]+'_tag', True)
        print(query)
        cur.execute(query)
        query = f"CREATE TABLE {post_id[1:]}_zip ( id INT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255) NOT NULL, contents LONGBLOB NOT NULL);" 
        cur.execute(query)
        query = f"CREATE TABLE {post_id[1:]}_img ( id INT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255) NOT NULL, contents LONGBLOB NOT NULL);" 
        cur.execute(query)
        file = request.files['zipfile']
        file_contents = file.read()
        if zipfile.is_zipfile(BytesIO(file_contents)):
            # Store the file contents in the database
            cursor = db.cursor()
            cursor.execute(f'INSERT INTO {post_id[1:]}_zip (filename, contents) VALUES (%s, %s)', (file.filename, file_contents))
            db.commit()
        file = request.files['imagefile']
        file_contents = file.read()
        if file:
            # Store the file contents in the database
            cursor = db.cursor()
            cursor.execute(f'INSERT INTO {post_id[1:]}_img (filename, contents) VALUES (%s, %s)', (file.filename, file_contents))
            db.commit()
        helper.create_linked_table(cur, post_id[1:], '_upv', 'A') # upvote list
        helper.create_linked_table(cur, post_id[1:], '_com', 'C') # comment list
        helper.create_linked_table(cur, post_id[1:], '_rep', 'A') # report list
        helper.create_linked_table(cur, post_id[1:], '_ins', 'I') # institute list
        helper.create_linked_table(cur, post_id[1:], '_tag', 'T') # tag list


        query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(session['user']['id_uniq']+"_pos", 'P', post_id[1:])
        cur.execute(query)
        for x in postTags:
            query = "SELECT * FROM Tag WHERE name = '{}';".format(x)
            cur.execute(query)
            existing = cur.fetchall()

            if len(existing) == 0:
                # tag does not exist
                tag_id = helper.id_gen(cur, 'T', session['user']['username'], 'Tag')
                query = "INSERT INTO Tag (id_obj, id_uniq, name, posts, members, api_visibility) VALUES ('{}', '{}', '{}', '{}', '{}', {});".format('T', tag_id[1:], x, tag_id[1:]+'_pos', tag_id[1:]+'_mem', True)
                cur.execute(query)
                helper.create_linked_table(cur, tag_id[1:], '_pos', 'P')
                helper.create_linked_table(cur, tag_id[1:], '_mem', 'A')
            else:
                # tag exists
                tag_obj = 'T'
                tag_uniq = existing[0]['id_uniq']
                tag_id = tag_obj + tag_uniq
            query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(post_id[1:]+'_tag', 'T', tag_id[1:])
            cur.execute(query)
            query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(tag_id[1:]+'_pos', 'P', post_id[1:])
            cur.execute(query)
            query = "SELECT * FROM {}_tag WHERE id_uniq = %s".format(session['user']['id_uniq'])
            cur.execute(query, (tag_id[1:],))
            if not cur.fetchall():
                query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(session['user']['id_uniq']+"_tag", "T", tag_id[1:])
                cur.execute(query)
        
        for x in postInst:
            # cur.execute(f"SELECT * FROM my_table WHERE name = %s", (column_value,))
            # if cur.fetchall()[0]['tn']:
            #     return ""
            query = "SELECT * FROM Institution WHERE name = '{}';".format(x)
            cur.execute(query)
            existing = cur.fetchall()

            if existing:
                # institute does not exist
            #     print('\n\n\n\n\n\n\n\n institute does not exist \n\n\n\n\n\n\n\n\n\n\n\n\n')
            # else:
                # institute exists
                inst_obj = 'I'

                inst_uniq = existing[0]['id_uniq']
                inst_id = inst_obj + inst_uniq
                query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(post_id[1:]+'_ins', 'I', inst_id[1:])
                cur.execute(query)

    mysql.connection.commit()
    cur.close()
    return redirect("/home")


@app.route('/js')
def start_js():
    return render_template('js/start.js')

@app.route('/js/main')
def main_js():
    return render_template('js/main.js')

@app.route('/about')
@login_required
def about():
    return render_template('html/about_us.html')

@app.route('/api')
@login_required
def apis():
    return render_template('html/apis.html')

@app.route('/apimethods')
@login_required
def api_meth():
    return render_template('html/apimethods.html')

@app.route('/apiobjects')
@login_required
def api_obj():
    return render_template('html/apiobj.html')

@app.route('/institution/create', methods=["POST", "GET"])
@login_required
def create_institution():
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    msg = ""
    if request.method == "POST":
        username_inst = request.form['username_inst']
        email_inst = request.form['email_inst']
        otp_inst = request.form['otp_inst']
        passcode_inst = request.form['passcode_inst']
        country_inst = request.form['country_inst']
        state_inst = request.form['state_inst']
        city_inst = request.form['city_inst']
        web_inst = request.form['web_inst']
        desc_inst = request.form['desc_inst']
        # git = request.form['git_signup']
        # org = request.form['org_signup']
        # image = request.form['image_profile_signup']
        # name = request.form['name_signup']
        if request.form['send_button_signup_inst'] == 'send_otp_signup_inst':
            if not helper.check_username(username_inst):
                msg = "Username can only contain alphabets, number and _"
            if not helper.unique_username(cur, username_inst):
                msg = "Username already exists"
            elif not email_inst:
                msg = "Please enter Email"
            else:
                msg = "Enter OTP"
                global otp_institute
                otp_institute[email_inst] = '123456'
                otp_sub = str(otp_institute[email_inst])+" is your OTP for Synergy Signup"
                otp_body = "Hi "+username_inst+"\nWelcome to Synergy,\n"+otp_sub
                #helper.mail(email,otp_sub, otp_body)
            cur.close()
            return render_template("html/create_institution.html", message1=msg, username=username_inst, email=email_inst, country=country_inst, state=state_inst, city=city_inst, web=web_inst, desc = desc_inst)
        elif request.form['send_button_signup_inst'] == 'create_account_signup_inst':
            if email_inst in otp_institute:
                if otp_inst == otp_institute[email_inst]:
                    if helper.password_strength(passcode_inst)!=1:
                        msg = "Password strength is low"
                        cur.close()
                        return render_template("html/create_institution.html", message1=msg, username=username_inst, email=email_inst, country=country_inst, state=state_inst, city=city_inst, web=web_inst, desc=desc_inst)
                    hash_password = helper.hash_pwd(passcode_inst)
                    id_uniq = helper.id_gen(cur, 'I', username_inst, "Institution")
                    query = "INSERT INTO Institution (id_obj, id_uniq, name, email_id, members,  posts, description, admin_obj, admin_uniq, visibility, api_visibility) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cur.execute(query,('I',id_uniq, username_inst, email_inst, id_uniq+"_mem", id_uniq+"_pos",desc_inst, 'A', session['user']['id_uniq'], True, True)) #how to get the account which is making the institution !
                    query = "INSERT INTO Personal (id_obj, id_uniq, pass) values (%s, %s, %s)"
                    cur.execute(query, ('I', id_uniq, hash_password))
                    query = "INSERT INTO Id (id_obj, id_uniq) values (%s, %s)"
                    cur.execute(query, ('A', id_uniq))
                    helper.create_linked_table(cur, id_uniq, "_mem", 'A')
                    helper.create_linked_table(cur, id_uniq, "_pos", 'P')
                    del otp_institute[email_inst]
                    cur.close()
                    mysql.connection.commit()
                    return redirect("/home")
                else:
                    msg = "Invalid OTP"
                    cur.close()
                    return render_template("html/create_institution.html", message1=msg, username_inst=username_inst, email_inst=email_inst, country_inst=country_inst, state_inst=state_inst, city_inst=city_inst, web=web_inst, desc=desc_inst)
            else:
                msg = "No valid OTP for "+email_inst
                cur.close()
                return render_template("html/create_institution.html", message1=msg, username=username_inst, email=email_inst, country=country_inst, state=state_inst, city=city_inst, web=web_inst, desc=desc_inst)
        msg = "There was some error please try again"
        cur.close()
        return render_template("html/create_institution.html", message1=msg)
    else:
        return render_template("html/create_institution.html", message1=msg)

@app.route('/js/institution/create')
@login_required
def create_institution_js():
    return render_template('js/create_institution.js')

@app.route('/header')
def header():
    return render_template('html/header.html')

@app.route('/js/header')
def header_js():
    return render_template('js/header.js', username = session['user']['username'])

@app.route('/home')
@login_required
def home():
    username = session['user']['username']
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    query = "SELECT * from Account WHERE BINARY username = %s"
    cur.execute(query,(username,))
    user = cur.fetchall()[0]
    global feed
    feed = helper.feed(cur, user)
    global stats
    stats = []
    stats.append(helper.contribution_inst(cur))
    stats.append(helper.contribution_user(cur))
    stats.append(helper.likes_inst(cur))
    stats.append(helper.likes_user(cur))
    cur.close()
    mysql.connection.commit()
    return render_template('html/home.html', feed = feed, follow = helper.follow_help, stats = stats, user = session['user'])

@app.route('/js/home')
@login_required
def home_js():
    return render_template('js/home.js.j2', feed = feed)

@app.route('/institute/<string:insti_id>')
@login_required
def institute(insti_id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in profile page")
    global institute_data
    global inst_post
    institute_data, inst_post = helper.institute_data(cur, insti_id, session['user'])
    cur.close()
    return render_template('html/institute.html', profile = institute_data, user = session['user'], feed = inst_post)

@app.route('/js/institute')
@login_required
def institute_js():
    return render_template('js/institute.js.j2', feed = inst_post, profile = institute_data)

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
@login_required
def loader4():
    return render_template('html/loader4.html')

@app.route('/js/load/home')
@login_required
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

@app.route('/post/<string:post_id>')
@login_required
def post(post_id): # id_uniq
    # changr code here
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM Post WHERE id_uniq = '{}';".format(post_id)
    cur.execute(query)
    global post_
    post = cur.fetchall()[0]

    tag_list = post['tag_list']

    query = "SELECT * FROM {} ;".format(tag_list)
    cur.execute(query)
    tag_ids = cur.fetchall()

    tags = []
    for x in tag_ids:
        query = "SELECT * FROM Tag WHERE id_uniq = '{}';".format(x['id_uniq'])
        cur.execute(query)
        tag = cur.fetchall()[0]
        # tag['id_uniq'],tag['name'] 
        tags.append((tag['id_uniq'],tag['name'].replace("&apos;", "'")))
    # print(tags)


    time = relativedelta(datetime.now(),post['creation_time'])
    if time.years:
        time_str = "{} year{}".format(time.years, "" if time.years==1 else "s")
    elif time.months:
        time_str = "{} month{}".format(time.months,  "" if time.months==1 else "s")
    elif time.days:
        time_str = "{} day{}".format(time.days,  "" if time.days==1 else "s")
    elif time.hours:
        time_str = "{} hour{}".format(time.hours,  "" if time.hours==1 else "s")
    elif time.minutes:
        time_str = "{} minute{}".format(time.minutes,  "" if time.minutes==1 else "s")
    else:
        time_str = "{} second{}".format(time.seconds,  "" if time.seconds==1 else "s")
    post['creation_time'] = time_str

    current_user = session['user']['id_uniq']

    query = "SELECT * FROM Account WHERE id_uniq = '{}';".format(post['author_uniq'])
    cur.execute(query)
    extracted = cur.fetchall()[0]


    name = extracted['username']
    follow_table = extracted['followers']
    query = "SELECT * FROM {} WHERE id_uniq = '{}';".format(follow_table, current_user)
    cur.execute(query)
    if cur.fetchall():
        follow_done = True
    else:
        follow_done = False

    query = "SELECT * FROM {} WHERE id_uniq = '{}';".format(post['upvotes'], current_user)
    cur.execute(query)
    if cur.fetchall():
        upvote_done = True
    else:
        upvote_done = False
    
    query = "SELECT * from {};".format(post['upvotes'])
    cur.execute(query)
    upv_ct = len(cur.fetchall())

    query = "SELECT * from {};".format(post['comments'])
    cur.execute(query)
    comments = cur.fetchall()
    global comment_list
    comment_list = []
    for comment in comments:
        comment_list.append(helper.comment_get(cur, comment))
        comment_list = sorted(comment_list, key = lambda x: x[0]['time_sort'], reverse=True)
    print(len(comment_list))
    # print(comment_list)
    [{'comment_list':comment_list}]

    mysql.connection.commit()
    cur.close()
    post['t'] = tags
    post['n'] = name
    post['u'] = upvote_done
    post['fd'] = follow_done
    post['uc'] = upv_ct
    post['c'] = comment_list
    post_ = post
    return render_template('html/post.html', post = post, tag_list = tags, aname = name, upv = upvote_done, follow = follow_done, user=session['user'], upvct = upv_ct, comments = comment_list)


@app.route('/postComments/<string:post_id>', methods=['GET'])
def postComments(post_id): # id_uniq
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM Post WHERE id_uniq = '{}';".format(post_id)
    cur.execute(query)
    global post_
    post = cur.fetchall()[0]
    query = "SELECT * from {};".format(post['comments'])
    cur.execute(query)
    comments = cur.fetchall()
    comment_list = []
    for comment in comments:
        comment_list.append(helper.comment_get(cur, comment))
        comment_list = sorted(comment_list, key = lambda x: x[0]['time_sort'], reverse=True)
    # print(len(comment_list))
    comment_list =[[{'comment_list':comment_list, 'author_name':""}]]
    return comment_list


@app.route('/DisplayImage/<string:post_id>')
def post_photo(post_id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = '{}' AND table_name = '{}_img') AS tn".format('Synergy_db', post_id))
    if not cur.fetchall()[0]['tn']:
        return ""
    cur.execute(f"SELECT 1 FROM {post_id}_img LIMIT 1")
    if cur.fetchone():
        cur.execute("SELECT contents FROM {}_img LIMIT 1".format(post_id))
        result = cur.fetchone()
        if result:
            contents = result['contents']
            return send_file(io.BytesIO(contents), mimetype='image/jpeg')
        else:
            return ""
    else:
        return ""



@app.route('/download/<string:post_id>')
def download(post_id):
    # Retrieve the contents of the file from the database
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    # cursor = db.cursor()
    cur.execute(f"SELECT 1 FROM {post_id}_zip LIMIT 1")
    if cur.fetchone():
        cur.execute("SELECT contents FROM {}_zip LIMIT 1".format(post_id))
        row = cur.fetchone()
        # if row is None:
        #     return 'File not found'
        if row is not None:
            contents = row['contents']

            # Check if the contents are a ZIP archive
            if zipfile.is_zipfile(io.BytesIO(contents)):
                cur.execute("SELECT filename FROM {}_zip LIMIT 1".format(post_id))
                row = cur.fetchone()
                filename = row['filename']
                # If the contents are a ZIP archive, send them as a file download
                return send_file(io.BytesIO(contents),download_name=filename, as_attachment=True)
            # If the contents are a regular file, display them in the browser
            return contents
        else:
            return None
    else:
        return None


@app.route('/zipname/<string:post_id>', methods=['GET'])
def zipname(post_id):
    # Retrieve the contents of the file from the database
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    # cursor = db.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = '{}' AND table_name = '{}_zip') AS tn".format('Synergy_db', post_id))
    if not cur.fetchall()[0]['tn']:
        return ""
    cur.execute(f"SELECT 1 FROM {post_id}_zip LIMIT 1")
    if cur.fetchone():
        cur.execute("SELECT contents FROM {}_zip LIMIT 1".format(post_id))
        row = cur.fetchone()
        # if row is None:
        #     return 'File not found'
        if row is not None:
            contents = row['contents']

            # Check if the contents are a ZIP archive
            if zipfile.is_zipfile(io.BytesIO(contents)):
                cur.execute("SELECT filename FROM {}_zip LIMIT 1".format(post_id))
                row = cur.fetchone()
                filename = row['filename']
                # If the contents are a ZIP archive, send them as a file download
                return filename
            # If the contents are a regular file, display them in the browser
            return ""
        else:
            return ""
    else:
        return ""

@app.route('/js/post')
@login_required
def post_js():
    return render_template('js/post.js.j2', comments = comment_list, post = post_)

@app.route('/profile/<string:username>')
@login_required
def profile(username):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in profile page")
    global profile_data
    global my_post
    profile_data, my_post = helper.profile_data(cur, username, session['user'])
    cur.close()
    return render_template('html/profile.html', profile = profile_data, user = session['user'], feed = my_post)

@app.route('/js/profile')
@login_required
def profile_js():
    return render_template('js/profile.js.j2', feed = my_post, profile = profile_data)

@app.route('/signup')
def signup():
    return render_template('html/signup.html')

@app.route('/js/signup')
def signup_js():
    return render_template('js/signup.js')

@app.route('/tag')
@login_required
def tag():
    return render_template('html/tag.html')

@app.route('/js/tag')
@login_required
def tag_js():
    return render_template('js/tag.js')

@app.route('/plz_login')
def please_login():
    return render_template('html/need_login.html')

@app.route('/login', methods = ['POST'])
def login_form():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in login page")
    if request.method == "POST":
        username = request.form["inp_start1"]
        password = request.form["inp_start2"]
        query = "SELECT * FROM Account WHERE BINARY username = %s"
        cur.execute(query, (username,))
        user = cur.fetchall()
        msg = ""
        if user:
            id_obj = user[0]['id_obj']
            id_uniq = user[0]['id_uniq']
            query = "SELECT pass FROM Personal WHERE BINARY id_obj = %s AND BINARY id_uniq = %s"
            cur.execute(query, (id_obj, id_uniq))
            ids = cur.fetchall()
            cur.close()
            if helper.hash_pwd(password)==ids[0]['pass']:
                session['user'] = user[0]
                login_user(User(user[0]['username']))
                return redirect("/home")
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
            print("Can not connect to database in login_otp page")
        if request.method == "POST":
            if request.form["submit_button_start"] == "submit_start1":
                email = request.form["email_start"]
                query = "SELECT * WHERE email_id = %s"
                cur.execute(query, (email,))
                user = cur.fetchall()
                if user:
                    msg = "Enter OTP"
                    global otp
                    otp[email] = "123456"
                    otp_sub = str(otp[email])+" is your OTP for Synergy Login"
                    otp_body = otp_sub
                    # helper.mail(email,otp_sub, otp_body)
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
                        query = "SELECT username FROM Account WHERE email_id = %s"
                        cur.execute(query, (email,))
                        user = cur.fetchall()
                        username = user[0]['username']
                        del otp[email]
                        cur.close()
                        return redirect("/home")
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

@app.route('/signup', methods = ['POST'])
def signup_form():
        try:
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in signup page")
        if request.method == "POST":
            username = request.form['username_signup']
            email = request.form['email_signup']
            otp = request.form['otp_signup']
            password = request.form['password_signup']
            conf_password = request.form['confirm_signup']
            country = request.form['country_signup']
            state = request.form['state_signup']
            city = request.form['city_signup']
            website = request.form['web_signup']
            git = request.form['git_signup']
            org = request.form['org_signup']
            name = request.form['name_signup']
            if request.form['send_button_signup'] == 'send_otp_signup':
                if not helper.check_username(username):
                    msg = "Username can only contain alphabets, number and _"
                if not helper.unique_username(cur, username):
                    msg = "Username already exists"
                elif not helper.unique_email_id(cur, email):
                    msg = "Email already exists"
                elif not email:
                    msg = "Please enter Email"
                else:
                    msg = "Enter OTP"
                    global otp_signup
                    otp_signup[email] = "123456"
                    otp_sub = str(otp_signup[email])+" is your OTP for Synergy Signup"
                    otp_body = "Hi "+username+"\nWelcome to Synergy,\n"+otp_sub
                    # helper.mail(email,otp_sub, otp_body)
                cur.close()
                return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, name=name)
            elif request.form['send_button_signup'] == 'create_account_signup':
                if email in otp_signup:
                    if otp == otp_signup[email]:
                        if password != conf_password:
                            msg = "Password and Confirm Password do not match"
                            cur.close()
                            return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org,  otp=otp, name=name)
                        elif helper.password_strength(password)!=1:
                            msg = "Password strength is low"
                            cur.close()
                            return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org,  otp=otp,name=name)
                        hash_password = helper.hash_pwd(password)
                        id_uniq = helper.id_gen(cur, 'A', username, "Account")
                        query = "insert into Account (id_obj, id_uniq, username, name, email_id, institutes, posts, upvotes, bookmarks, followers, following, comments, visited_post, activity, tag_list, country, state, city, website_address, github_handle, organisation, visibility, report_list, api_visibility) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cur.execute(query,('A',id_uniq, username, name, email, id_uniq+"_ins", id_uniq+"_pos", id_uniq+"_upv", id_uniq+"_boo", id_uniq+"_ers", id_uniq+"_ing", id_uniq+"_com", id_uniq + "_vis", id_uniq+"_act", id_uniq+"_tag", country, state, city, website, git, org, True, id_uniq+"_rep", True))
                        query = "INSERT INTO Personal (id_obj, id_uniq, pass) values (%s, %s, %s)"
                        cur.execute(query, ('A', id_uniq, hash_password))
                        query = "INSERT INTO Id (id_obj, id_uniq) values (%s, %s)"
                        cur.execute(query, ('A', id_uniq))
                        helper.create_linked_table(cur, id_uniq, "_ins", 'I')
                        helper.create_linked_table(cur, id_uniq, "_pos", 'P')
                        helper.create_linked_table(cur, id_uniq, "_boo", 'P')
                        helper.create_linked_table(cur, id_uniq, "_ers", 'A')
                        helper.create_linked_table(cur, id_uniq, "_ing", 'A')
                        helper.create_linked_table(cur, id_uniq, "_com", 'C')
                        helper.create_linked_table(cur, id_uniq, "_vis", 'P')
                        helper.create_linked_table(cur, id_uniq, "_act", 'IP')
                        helper.create_linked_table(cur, id_uniq, "_tag", 'T')
                        helper.create_linked_table(cur, id_uniq, "_rep", 'R')
                        query = "CREATE TABLE {}_upv ( id_obj ENUM(%s) DEFAULT %s NOT NULL, id_uniq VARCHAR(200) NOT NULL UNIQUE, PRIMARY KEY (id_obj, id_uniq), count INT NOT NULL)".format(id_uniq)
                        cur.execute(query,('A','A'))
                        query = f"CREATE TABLE {id_uniq}_img ( id INT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255) NOT NULL, contents LONGBLOB NOT NULL);" 
                        cur.execute(query)
                        file_var = request.files['image_profile_signup']
                        filename = file_var.filename
                        if file_var:
                            query = "Insert into {}_img (filename, contents) values (%s, %s)".format(id_uniq)
                            cur.execute(query, (filename, file_var.read()))
                        else:
                            # cur.execute("SELECT contents FROM {}_img LIMIT 1".format("AAxefaultPh4253718819"))
                            # result = cur.fetchone()
                            # with open('./DefaultPhoto.png', 'rb') as f:
                            #     image_data = f.read()
                            # image_data_blob = mysql.connector.Binary(image_data)
                            image_data = generate_image()
                            cursor = db.cursor()
                            cursor.execute(f'INSERT INTO {id_uniq}_img (filename, contents) VALUES (%s, %s)', ("DefaultPhoto", image_data))
                            db.commit()
                        del otp_signup[email]
                        cur.close()
                        mysql.connection.commit()
                        return redirect("/")
                    else:
                        msg = "Invalid OTP"
                        cur.close()
                        return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, name=name)
                else:
                    msg = "No valid OTP for "+email
                    cur.close()
                    return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, name=name)
            msg = "There was some error please try again"
            cur.close()
            return render_template("html/signup.html", message1=msg)

@app.route('/comment/post/<string:post_id>', methods=["POST"])
def comment_for_post(post_id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    helper.comment_to_post(cur, session['user']['id_uniq'], post_id, request.form['add_comment_post'], session['user']['username'])
    cur.close()
    mysql.connection.commit()
    return redirect('/post/'+post_id)

@app.route('/comment/comment/<string:comm_id>', methods=["POST"])
def comment_for_comment(comm_id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    helper.comment_to_comment(cur, session['user']['id_uniq'], comm_id, request.form['button_comment_post2'], session['user']['username'])
    cur.close()
    mysql.connection.commit()
    return redirect('/post/'+post_['id_uniq'])

@app.route('/pfp')
def profile_photo():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    cur.execute("SELECT contents FROM {}_img LIMIT 1".format(session['user']['id_uniq']))
    result = cur.fetchone()
    if result:
        contents = result['contents']
    else:
        contents = generate_image()
    return send_file(io.BytesIO(contents), mimetype='image/jpeg')

@app.route('/pfpPost')
def profile_photoPost():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    cur.execute("SELECT contents FROM {}_img LIMIT 1".format(post_['author_uniq']))
    result = cur.fetchone()
    if result:
        contents = result['contents']
    else:
        contents = generate_image()
    return send_file(io.BytesIO(contents), mimetype='image/jpeg')


@app.route('/pfpFeed/<string:id_uniq>')
def profile_photoFeed(id_uniq):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    query = f"SELECT 1 FROM {id_uniq}_img LIMIT 1"
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = '{}' AND table_name = '{}_img') AS tn".format('Synergy_db', id_uniq))
    result = cur.fetchall()
    if result[0]['tn']:
        cur.execute("SELECT contents FROM {}_img LIMIT 1".format(id_uniq))
        result = cur.fetchone()
        if result:
            contents = result['contents']
        return send_file(io.BytesIO(contents), mimetype='image/jpeg')
   
    contents = generate_image()
    return send_file(io.BytesIO(contents), mimetype='image/jpeg')
    

# For searching Institutes/Name/Username
@app.route('/search', methods=['POST'])
def search_results():
     query = request.form.get('query')
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     to_show = []
     id_uniq = []
     renderes = []
     sql = "SELECT * FROM Account WHERE username LIKE %s"
     val = ('%' + query + '%',)
     cursor.execute(sql, val)
     # fetch the results of the query
     results = cursor.fetchall()
     for i in range(len(results)):
         to_show.append(results[i]['username'])
         id_uniq.append(results[i]['username'])
         renderes.append('profile')
     
     sql = "SELECT * FROM Institution WHERE name LIKE %s"
     val = ('%' + query + '%',)
     cursor.execute(sql, val)
     # fetch the results of the query
     results = cursor.fetchall()
     for i in range(len(results)):
         to_show.append(results[i]['name'])
         id_uniq.append(results[i]['id_uniq'])
         renderes.append('institute')
     return jsonify({'results': to_show, 'id_uniqs':id_uniq, 'renderes':renderes})

# For searching in Posts
@app.route('/searchPost', methods=['POST'])
def searchPost_results():
     query = request.form.get('query')
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     to_show = []
     id_uniqs = []
     x = feed
     for my_tuple in x:
        if query in my_tuple[5]:
            if len(my_tuple[5]) == 0:
                input_string = my_tuple[6]
                words = input_string.split("<br>")
                output_string = ' '.join(words)
                to_show.append(output_string[0:min(50, len(my_tuple[6]))])
                id_uniqs.append(my_tuple[0])
            else:
                input_string = my_tuple[5]
                words = input_string.split("\n")
                output_string = ' '.join(words)
                to_show.append((output_string.replace('<br>', ' '))[0:min(50, len(my_tuple[5]))])
                id_uniqs.append(my_tuple[0])
        elif query in my_tuple[6]:
            if len(my_tuple[5]) == 0:
                input_string = my_tuple[6]
                words = input_string.split("\n")
                output_string = ' '.join(words)
                to_show.append((input_string.replace('<br>', ' '))[0:min(50, len(my_tuple[6]))])
                id_uniqs.append(my_tuple[0])
            else:
                input_string = my_tuple[5]
                words = input_string.split("\n")
                output_string = ' '.join(words)
                to_show.append((output_string.replace('<br>', ' '))[0:min(50, len(my_tuple[5]))])
                id_uniqs.append(my_tuple[0])
     return jsonify({'results': to_show, 'id_uniqs': id_uniqs})


@app.route('/home/SORT=<string:sort>')
@login_required
def home_sort(sort):
    username = session['user']['username']
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    query = "SELECT * from Account WHERE BINARY username = %s"
    cur.execute(query,(username,))
    user = cur.fetchall()[0]
    global feed
    feed = helper.feed(cur, user)
    if sort=="time":
        feed = sorted(feed, key = lambda x : x[7])
    elif sort=="upvotes":
        feed = sorted(feed, key = lambda x : x[1], reverse=True)
    return render_template('html/home.html', feed = feed, follow = helper.follow_help, stats = stats, user = session['user'])    

@app.route('/profile/<string:username>/SORT=<string:sort>')
@login_required
def profile_sort(username, sort):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    query = "SELECT * from Account WHERE BINARY username = %s"
    cur.execute(query,(username,))
    user = cur.fetchall()[0]
    global my_post
    global profile_data
    profile_data, my_post = helper.profile_data(cur, username, session['user'])
    if sort=="time":
        my_post = sorted(my_post, key = lambda x : x[7])
    elif sort=="upvotes":
        my_post = sorted(my_post, key = lambda x : x[1], reverse=True)
    return render_template('html/profile.html', feed = my_post, user = session['user'], profile = profile_data)   

@app.route('/institute/<string:id>/SORT=<string:sort>')
@login_required
def institute_sort(id, sort):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    global institute_data
    global inst_post
    institute_data, inst_post = helper.institute_data(cur, id, session['user'])
    if sort=="time":
        inst_post = sorted(inst_post, key = lambda x : x[7])
    elif sort=="upvotes":
        inst_post = sorted(inst_post, key = lambda x : x[1], reverse=True)
    return render_template('html/institute.html', feed = inst_post, user = session['user'], profile = institute_data) 

@app.route('/translate/post/<string:content>')
@login_required
def translate(content):
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"
    querystring = {"to[0]": "hi", "api-version": "3.0", "from": "en", "profanityAction": "NoAction", "textType": "plain"}
    payload = [{"Text": content}]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "1db8e49b5amsh647a1bc64905b0bp18c86ejsn40decaddaceb",
        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers, params=querystring)
    global post_
    post_['content'] = response.text[27:-15]
    return render_template('html/post.html', post = post_, tag_list = post_['t'], aname = post_['n'], upv = post_['u'], follow = post_['fd'], user=session['user'], upvct = post_['uc'], comments = post_['c'])
    # return redirect("/post/"+post_['id_uniq'])
    # return {"translated_text": response.json()}

@app.route('/profile/delete_insti/<string:insti_id>')
@login_required
def remove_insti(insti_id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in remove_insti page")
    query = "DELETE FROM {} WHERE id_uniq = %s".format(session['user']['institutes'])
    cur.execute(query, (insti_id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/profile/'+session['user']['username'])

@app.route('/profile/delete_follower/<string:id>')
@login_required
def remove_follower(id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in remove_follower page")
    # query = "DELETE FROM {} WHERE id_uniq = %s".format(session['user']['followers'])
    # cur.execute(query, (id,))
    helper.unfollow_help(cur, id, session['user']['id_uniq'])
    mysql.connection.commit()
    cur.close()
    return redirect('/profile/'+session['user']['username'])

@app.route('/profile/delete_following/<string:id>')
@login_required
def remove_following(id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in remove_follower page")
    # query = "DELETE FROM {} WHERE id_uniq = %s".format(session['user']['following'])
    # cur.execute(query, (id,))
    helper.unfollow_help(cur, session['user']['id_uniq'], id)
    mysql.connection.commit()
    cur.close()
    return redirect('/profile/'+session['user']['username'])

@app.route('/post/upvote_post/<string:post_id>')
@login_required
def upvote_from_post_page(post_id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in upvote_post page")
    if post_['u']:
        helper.downvote_for_post_help(cur, session['user']['id_uniq'], post_id)
    else:
        helper.upvote_for_post_help(cur, session['user']['id_uniq'], post_id)
    mysql.connection.commit()
    cur.close()
    return redirect('/post/'+post_id)

@app.route('/post/follow_user/<string:id>/<string:post_id>')
@login_required
def follow_from_post_page(id, post_id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in follow_post page")
    if post_['fd']:
        helper.unfollow_help(cur, session['user']['id_uniq'], id)
    else:
        helper.follow_help(cur, session['user']['id_uniq'], id)
    mysql.connection.commit()
    cur.close()
    return redirect('/post/'+post_id)

@app.route('/profile/follow/<string:id>')
@login_required
def follow_from_profile(id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in follow_profile page")
    if profile_data['isfollow']:
        helper.unfollow_help(cur, session['user']['id_uniq'], id)
    else:
        helper.follow_help(cur, session['user']['id_uniq'], id)
    mysql.connection.commit()
    cur.close()
    return redirect('/profile/'+profile_data['username'])

@app.route('/institute/follow/<int:count>')
@login_required
def follow_account_inst(count):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in follow_profile page")
    if inst_post[count][8]:
        helper.unfollow_help(cur, session['user']['id_uniq'], inst_post[count][9])
    else:
        helper.follow_help(cur, session['user']['id_uniq'], inst_post[count][9])
    mysql.connection.commit()
    cur.close()
    return redirect('/institute/'+institute_data['id_uniq'])

@app.route('/institute/join/<string:id>')
@login_required
def join_institute(id):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in join_institute page")
    if institute_data['isfollow']:
        query = "DELETE FROM {} WHERE BINARY id_uniq = %s".format(session['user']['institutes'])
        cur.execute(query, (id,))
    else:
        query = "INSERT INTO {} (id_obj, id_uniq) values (%s, %s)".format(session['user']['institutes'])
        cur.execute(query, ('I', id))
    mysql.connection.commit()
    cur.close()
    return redirect('/institute/'+institute_data['id_uniq'])

@app.route('/profile/upvote_post2/<int:count>')
@login_required
def upvote_for_post_from_profile(count):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    post_num = count
    if my_post[post_num][2]:
        helper.downvote_for_post_help(cur, session['user']['id_uniq'], my_post[post_num][0])
    else:
        helper.upvote_for_post_help(cur, session['user']['id_uniq'], my_post[post_num][0])
    mysql.connection.commit()
    cur.close()
    
    return redirect("/profile/"+profile_data['username'])

@app.route('/post/comment/upv/<string:comment_id>')
def upvote_for_comment(comment_id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * from Comment where id_uniq = %s"
    cur.execute(query, (comment_id,))
    comment_d = cur.fetchall()[0]
    query = "SELECT * from {} where id_uniq = %s".format(comment_d['upvotes'])
    cur.execute(query, (session['user']['id_uniq'],))
    if cur.fetchall():
        helper.downvote_for_comment(cur, session['user']['id_uniq'], comment_id)
    else:
        helper.upvote_for_comment(cur, session['user']['id_uniq'], comment_id)
    cur.close()
    mysql.connection.commit()
    return redirect('/post/'+post_['id_uniq'])

@app.route('/institute/upvote_post2/<int:count>')
@login_required
def upvote_for_post_from_inst(count):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    post_num = count
    if inst_post[post_num][2]:
        helper.downvote_for_post_help(cur, session['user']['id_uniq'], inst_post[post_num][0])
    else:
        helper.upvote_for_post_help(cur, session['user']['id_uniq'], inst_post[post_num][0])
    mysql.connection.commit()
    cur.close()
    
    return redirect("/institute/"+institute_data['id_uniq'])

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

def test_db():
    with app.app_context():
        try:
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in test_db")
            return
        with app.open_resource('DatabaseExtend.sql', mode='r') as sql_file:
            cur.execute(sql_file.read())
        cur.close()
        mysql.connection.commit()
        sql_file.close()
    with app.app_context():
        try:
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in test_db")
            return
        with app.open_resource('FeedExtraData.sql', mode='r') as sql_file:
            cur.execute(sql_file.read())
        cur.close()
        mysql.connection.commit()
        sql_file.close()


def insertImage():
    # Insert the images into the database
    id_uniq_num = 1111111111
    cursor = db.cursor()
    for i in range(1, 101):
        id_uniq_num += i - 1
        image_data = generate_image()
        cursor.execute(f"DROP TABLE IF EXISTS aaaaaaaaaa{id_uniq_num}_img;")
        cursor.execute(f"CREATE TABLE aaaaaaaaaa{id_uniq_num}_img ( id INT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255) NOT NULL, contents LONGBLOB NOT NULL);" )
        cursor.execute(f'INSERT INTO aaaaaaaaaa{id_uniq_num}_img (filename, contents) VALUES (%s, %s)', ("DefaultPhoto", image_data))
    db.commit()


if __name__ == "__main__":
    # init_db()
    # test_db()
    # insertImage()
    app.run(debug=True)
