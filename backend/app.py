from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import helper
from datetime import datetime
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
app.secret_key = "devang"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345678"
app.config["MYSQL_DB"] = "Synergy_db"
mysql = MySQL(app)

otp = {}
otp_signup = {}
feed = []


@app.route('/')
def start():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
        return
    print('start ')
    print('end ')
    return render_template('html/start.html', message1="", message2="", show_forget=False)



@app.route('/home/post', methods = ['POST'])
def post_input():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        postTitle = request.form['posttit']
        postTags = request.form['posttags']
        postTags = postTags.split(";")
        postTags = [x.strip() for x in postTags]
        postDescription = request.form['post_description']


        Tags = []
        for x in postTags:
            if x != "":
                Tags.append(x)
        postTags = Tags
        postInst = request.form['postinst']
        postInst = postInst.split(";")
        postInst = [x.strip() for x in postInst]
        institute = []
        for x in postInst:
            if x != "":
                institute.append(x)
        postInst = institute
        author_id = session['user']['id_uniq']
        post_id = helper.id_gen(cur, 'P', session['user']['username'], 'Post')
        print('data fetched !')
        print(postTitle, postTags, postDescription, postInst, author_id, post_id)
        query = "INSERT INTO Post (id_obj, id_uniq, author_obj, author_uniq, title, content, upvotes, comments, report_list, public_post, visibility,  institutes, tag_list, api_visibility) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', '{}', {});".format('P', post_id[1:], 'A', author_id, postTitle, postDescription, post_id[1:]+'_upv', post_id[1:]+'_com', post_id[1:]+'_rep', True, True, post_id[1:]+'_ins', post_id[1:]+'_tag', True)
        print(query)
        cur.execute(query)
        helper.create_linked_table(cur, post_id[1:], '_upv', 'A') # upvote list
        helper.create_linked_table(cur, post_id[1:], '_com', 'C') # comment list
        helper.create_linked_table(cur, post_id[1:], '_rep', 'A') # report list
        helper.create_linked_table(cur, post_id[1:], '_ins', 'I') # institute list
        helper.create_linked_table(cur, post_id[1:], '_tag', 'T') # tag list


        for x in postTags:
            query = "SELECT * FROM Tag WHERE name = '{}';".format(x)
            cur.execute(query)
            existing = cur.fetchall()
            print('-'*100)
            print(existing)

            if len(existing) == 0:
                # tag does not exist
                tag_id = helper.id_gen(cur, 'T', session['user']['username'], 'Tag')
                query = "INSERT INTO Tag (id_obj, id_uniq, name, posts, members, api_visibility) VALUES ('{}', '{}', '{}', '{}', '{}', {});".format('T', tag_id[1:], x, tag_id[1:]+'_pos', tag_id[1:]+'_mem', True)
                print(query, '\n\n\n\n tag does not exist')
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
        
        for x in postInst:
            query = "SELECT * FROM Institution WHERE name = '{}';".format(x)
            cur.execute(query)
            existing = cur.fetchall()
            print('-'*100)
            print(existing)

            if len(existing) == 0:
                # institute does not exist
                print('\n\n\n\n\n\n\n\n institute does not exist \n\n\n\n\n\n\n\n\n\n\n\n\n')
            else:
                # institute exists
                inst_obj = 'I'
                inst_uniq = existing[0]['id_uniq']
                inst_id = inst_obj + inst_uniq
            query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(post_id[1:]+'_ins', 'I', inst_id[1:])
            cur.execute(query)

    mysql.connection.commit()
    cur.close()
    return redirect("/home/"+session['user']['username'])



@app.route('/js')
def start_js():
    return render_template('js/start.js')

@app.route('/js/main')
def main_js():
    return render_template('js/main.js')

@app.route('/about')
def about():
    return render_template('html/about_us.html')

@app.route('/api/introduction')
def apis():
    return render_template('html/apis.html', username = session['user']['username'])

@app.route('/api/methods')
def api_method():
    return render_template('html/apimethods.html', username =session['user']['username'])

@app.route('/institution/create')
def create_institution():
    return render_template('html/create_institution.html')

@app.route('/js/institution/create')
def create_institution_js():
    return render_template('js/create_institution.js')

@app.route('/header')
def header():
    return render_template('html/header.html')

@app.route('/js/header')
def header_js():
    return render_template('js/header.js', username = session['user']['username'])

@app.route('/home/<string:username>')
def home(username):
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    query = "SELECT * from Account WHERE BINARY username = %s"
    cur.execute(query,(username,))
    user = cur.fetchall()[0]
    session['user'] = user
    global feed
    feed = helper.feed(cur, user)
    return render_template('html/home.html', feed = feed, follow = helper.follow)

@app.route('/js/home')
def home_js():
    return render_template('js/home.js.j2', feed = feed)

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

@app.route('/post/<string:post_id>')
def post(post_id): # id_uniq
    # changr code here
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print(post_id , '\n\n\n\n')
    query = "SELECT * FROM Post WHERE id_uniq = '{}';".format(post_id)
    cur.execute(query)
    post = cur.fetchall()[0]

    tag_list = post['tag_list']

    print(tag_list)
    query = "SELECT * FROM {} ;".format(tag_list)
    cur.execute(query)
    tag_ids = cur.fetchall()
    print(tag_ids)

    tags = []
    for x in tag_ids:
        query = "SELECT * FROM Tag WHERE id_uniq = '{}';".format(x['id_uniq'])
        cur.execute(query)
        tag = cur.fetchall()[0]
        tags.append((tag['id_uniq'],tag['name']))
    print('\n\n\n\n', tags, '\n\n\n\n\n')


    time = relativedelta(datetime.now(),post['creation_time'])
    print(time, post['creation_time'], '\n\n\n\n\n\n\n\n\n\n\n')
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

    print('\n\n\n\n\n',extracted, '\n\n\n\n\n')

    name = extracted['username']
    follow_table = extracted['followers']
    query = "SELECT * FROM {} WHERE id_uniq = '{}';".format(follow_table, current_user)
    print(query)
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
    print("\n",query,"\n")
    cur.execute(query)
    comments = cur.fetchall()
    for comment_id in comments:
        helper.comment_get(cur, comment_id)

    mysql.connection.commit()
    cur.close()
    return render_template('html/post.html', post = post, tag_list = tags, aname = name, upv = upvote_done, follow = follow_done, user=session['user'], upvct = upv_ct)

@app.route('/js/post')
def post_js():
    return render_template('js/post.js')

@app.route('/profile/<string:username>')
def profile(username):
    return render_template('html/profile.html')

@app.route('/js/profile')
def profile_js():
    return render_template('js/profile.js')

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
        print("Can not connect to database in login page")
    if request.method == "POST":
        username = request.form["inp_start1"]
        password = request.form["inp_start2"]
        query = "SELECT id_obj, id_uniq,  username FROM Account WHERE BINARY username = %s"
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
                return redirect("/home/"+user[0]['username'])
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
                query = "SELECT email_id FROM Account WHERE email_id = %s"
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
                        return redirect("/home/"+username)
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
            image = request.form['image_profile_signup']
            name = request.form['name_signup']
            if request.form['send_button_signup'] == 'send_otp_signup':
                if not helper.check_username(username):
                    msg = "Username can only contain alphabets, number and _"
                if not helper.unique_username(cur, username):
                    msg = "Username already exists"
                elif not email:
                    msg = "Please enter Email"
                else:
                    msg = "Enter OTP"
                    global otp_signup
                    otp_signup[email] = '123456'
                    otp_sub = str(otp_signup[email])+" is your OTP for Synergy Signup"
                    otp_body = "Hi "+username+"\nWelcome to Synergy,\n"+otp_sub
                    # helper.mail(email,otp_sub, otp_body)
                cur.close()
                return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, image=image, name=name)
            elif request.form['send_button_signup'] == 'create_account_signup':
                if email in otp_signup:
                    if otp == otp_signup[email]:
                        if password != conf_password:
                            msg = "Password and Confirm Password do not match"
                            cur.close()
                            return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, image=image, otp=otp, name=name)
                        elif helper.password_strength(password)!=1:
                            msg = "Password strength is low"
                            cur.close()
                            return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, image=image, otp=otp,name=name)
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
                        helper.create_linked_table(cur, id_uniq, "_upv", 'A')
                        helper.create_linked_table(cur, id_uniq, "_boo", 'P')
                        helper.create_linked_table(cur, id_uniq, "_ers", 'A')
                        helper.create_linked_table(cur, id_uniq, "_ing", 'A')
                        helper.create_linked_table(cur, id_uniq, "_com", 'C')
                        helper.create_linked_table(cur, id_uniq, "_vis", 'P')
                        helper.create_linked_table(cur, id_uniq, "_act", 'IP')
                        helper.create_linked_table(cur, id_uniq, "_tag", 'T')
                        helper.create_linked_table(cur, id_uniq, "_rep", 'R')
                        del otp_signup[email]
                        cur.close()
                        mysql.connection.commit()
                        return redirect("/")
                    else:
                        msg = "Invalid OTP"
                        cur.close()
                        return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, image=image, name=name)
                else:
                    msg = "No valid OTP for "+email
                    cur.close()
                    return render_template("html/signup.html", message1=msg, username=username, email=email, country=country, state=state, city=city, website=website, git=git, org=org, image=image, name=name)
            msg = "There was some error please try again"
            cur.close()
            return render_template("html/signup.html", message1=msg)

@app.route('/home/<string:username>/SORT=<string:sort>')
def home_sort(username, sort):
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
    for i in feed:
        print(i[0], i[5])
    return render_template('html/home.html', feed = feed, follow = helper.follow)    

@app.route('/follow', methods = ['POST'])
def follow():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in follow page")
    sender_id = session['user']['uniq_id']
    reciever_id = request.form['post_id']
    helper.follow(cur, sender_id, reciever_id)
    return jsonify({})

@app.route('/unfollow', methods = ['POST'])
def unfollow():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in unfollow page")
    sender_id = session['user']['uniq_id']
    reciever_id = request.form['post_id']
    helper.unfollow(cur, sender_id, reciever_id)
    return jsonify({})

@app.route('/upvote/post', methods = ['POST'])
def upvote_for_post():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in unfollow page")
    sender_id = session['user']['uniq_id']
    post_id = request.form['post_id']
    helper.upvote_for_post(cur, sender_id, post_id)
    return jsonify({})

@app.route('/downvote/post', methods = ['POST'])
def downvote_for_post():
    try:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in unfollow page")
    sender_id = session['user']['uniq_id']
    post_id = request.form['post_id']
    helper.downvote_for_post(cur, sender_id, post_id)
    return jsonify({})

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

if __name__ == "__main__":
    init_db()
    test_db()
    app.run(debug=True)