from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import helper
import sqlite3
# import unittest
connection = sqlite3.connect('Synergy_db')
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'

# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "12345678"
# app.config["MYSQL_DB"] = "Synergy_db"
# mysql = MySQL(app)

otp = {}
otp_signup = {}

def follow(sender_id, profile_id):
    ''' inputs are the uniq values ! '''
    try:
        cur = connection.cursor()
    except:
        print('some error happend in cursor !')
        return
    profile_followers = profile_id + str('_ers')
    sender_following = sender_id + str('_ing')
    query = ("SELECT * from {} WHERE id_uniq= '{}' ;".format(profile_followers, sender_id))
    cur.execute(query)
    value = cur.fetchall()
    if len(value) == 0 :
        query = ("INSERT INTO {} (id_obj, id_uniq) VALUES ( '{}', '{}');".format(profile_followers, 'A', sender_id))
        cur.execute(query)
        # insert into the following list !
        query = "SELECT * from {} WHERE id_uniq= '{}' ;".format(sender_following, profile_id)
        cur.execute(query)
        value = cur.fetchall()
        if len(value) == 0 :
            query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(sender_following, 'A', profile_id)
            cur.execute(query)
        else:
            print('#'*20 + '\n   DATABASE IS CORRUPTED !!\n')
    else:
        uniq = profile_id
        query = "SELECT name FROM Account WHERE id_uniq = '{}' ;".format(uniq)
        cur.execute(query)
        account_name = cur.fetchall()
        print('You have already followed {}'.format(account_name[0]['name']))
    connection.commit()
    cur.close()
    return

def unfollow(sender_id, profile_id):
    ''' Inputs values are id_uniq type !'''
    try:
        cur = connection.cursor()
    except:
        print('some error happended in cursor !')
        return
    # following from mani's ac to mecan's ac
    sender_following = sender_id + str('_ing')
    profile_followers = profile_id + str('_ers')
    query = ("SELECT * from {} WHERE id_uniq= '{}' ;".format(profile_followers, sender_id))
    cur.execute(query)
    value = cur.fetchall()
    # print('val', value)
    if len(value) > 0 :
        query = "DELETE FROM {} WHERE id_uniq = '{}';".format(profile_followers, value[0]['id_uniq'])
        cur.execute(query)
        # deleting from the following list !
        query = ("SELECT * from {} WHERE id_uniq= '{}' ;".format(sender_following, profile_id))
        cur.execute(query)
        value = cur.fetchall()
        if len(value) > 0:
            query = "DELETE FROM {} WHERE id_uniq = '{}';".format(sender_following, value[0]['id_uniq'])
            cur.execute(query)
        else:
            print('#'*20 + '\n   DATABASE IS CORRUPTED !!\n')
    else:
        query = "SELECT name FROM Account WHERE id_uniq = '{}' ;".format(profile_id)
        cur.execute(query)
        account_name = cur.fetchall()
        print("Already unfollowed {}".format(account_name[0]['name']))
    connection.commit()
    cur.close()
    return 

def upvote_for_post(sender_id, post_id):
    ''' requirements post_upvote_table, post_publisher_upvotes_table (obj, uniq, count = 0)'''
    try:
        cur = connection.cursor()
    except:
        print('error happened !')
        return 
    post_upvote_table = post_id + str('_upv')
    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(post_upvote_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    upvoted = False
    if len(value) == 0:
        query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('A', '{}') ;".format(post_upvote_table, sender_id)
        cur.execute(query)
        print('upvoted')
        upvoted = True
    else :
        print('already upvoted to post')
        connection.commit()
        cur.close() 
        return 
    
    query = "SELECT author_uniq FROM Post WHERE id_uniq = '{}' ;".format(post_id)
    cur.execute(query)
    value = cur.fetchall()
    post_publisher_id = value[0]['author_uniq']
    post_publisher_upvotes_table = post_publisher_id + str('_upv')


    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(post_publisher_upvotes_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    if len(value) == 0 :
        query = "INSERT INTO {} (id_obj, id_uniq, count) VALUES ('A', '{}', 1) ;".format(post_publisher_upvotes_table, sender_id)
        cur.execute(query)
    elif upvoted:
        count = value[0]['count']
        count += 1
        query = "UPDATE {} SET count = {} WHERE id_uniq = '{}' ;".format(post_publisher_upvotes_table,  count, sender_id)
        cur.execute(query)
        print('checked !')
    connection.commit()
    cur.close()
    return 

def upvote_for_comment(sender_id, comment_id):
    '''requirements comments_upvote table, comment_publisher_upvote table (obj, uniq, count = 0)'''
    try:
        cur = connection.cursor()
    except:
        print('error happened !')
        return 
    comment_upvote_table = comment_id + str('_upv')
    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(comment_upvote_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    upvoted = False
    if len(value) == 0:
        query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('A', '{}') ;".format(comment_upvote_table, sender_id)
        cur.execute(query)
        print('upvoted to coomment')
        upvoted = True
    else :
        print('already upvoted to comment')
        connection.commit()
        cur.close()
        return 
    
    query = "SELECT author_uniq FROM Comment WHERE id_uniq = '{}' ;".format(comment_id)
    cur.execute(query)
    value = cur.fetchall()
    comment_publisher_id = value[0]['author_uniq']
    comment_publisher_upvotes_table = comment_publisher_id + str('_upv')

    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(comment_publisher_upvotes_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    if len(value) == 0 :
        query = "INSERT INTO {} (id_obj, id_uniq, count) VALUES ('A', '{}', 1) ;".format(comment_publisher_upvotes_table, sender_id)
        cur.execute(query)
    elif upvoted:
        count = value[0]['count']
        count += 1
        query = "UPDATE {} SET count = {} WHERE id_uniq = '{}' ;".format(comment_publisher_upvotes_table,  count, sender_id)
        cur.execute(query)
        print('checked !')
    connection.commit()
    cur.close()
    return 
    
def downvote_for_post(sender_id, post_id):
    ''' requirements post_upvote_table, post_publisher_upvote_table '''
    try:
        cur = connection.cursor()
    except:
        print('error happened !')
        return 
    post_upvote_table = post_id + str('_upv')
    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(post_upvote_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    downvoted = False
    if len(value) > 0:
        query = "DELETE FROM {} WHERE id_uniq = '{}' ;".format(post_upvote_table, sender_id)
        cur.execute(query)
        print('downvoted post')
        downvoted = True
    else:
        print('already downvoted to post !')
        connection.commit()
        cur.close()
        return 
    
    # finding post_publisher_id 
    query = "SELECT author_uniq FROM Post WHERE id_uniq = '{}' ;".format(post_id)

    cur.execute(query)
    value = cur.fetchall()
    post_publisher_id = value[0]['author_uniq']
    post_publisher_upvotes_table = post_publisher_id + str('_upv')

    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(post_publisher_upvotes_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    if len(value) > 0 and downvoted:
        count = value[0]['count']
        count -= 1
        query = "UPDATE {} SET count = {} WHERE id_uniq = '{}' ;".format(post_publisher_upvotes_table,  count, sender_id)
        cur.execute(query)
        print('checked !')
    elif len(value) == 0 :
        print('database error !')
    connection.commit()
    cur.close()
    return 

def downvote_for_comment(sender_id, comment_id):
    ''' requirements comment_upvote_table, comment_publisher_upvote_table '''
    try:
        cur = connection.cursor()
    except:
        print('error happened !')
        return 
    comment_upvote_table = comment_id + str('_upv')
    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(comment_upvote_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    downvoted = False
    if len(value) > 0:
        query = "DELETE FROM {} WHERE id_uniq = '{}' ;".format(comment_upvote_table, sender_id)
        cur.execute(query)
        print('downvoted comment')
        downvoted = True
    else:
        print('already downvoted to comment !')
        connection.commit()
        cur.close()
        return 
    
    # finding comment_publisher_id 
    query = "SELECT author_uniq FROM Comment WHERE id_uniq = '{}' ;".format(comment_id)

    cur.execute(query)
    value = cur.fetchall()
    comment_publisher_id = value[0]['author_uniq']
    comment_publisher_upvotes_table = comment_publisher_id + str('_upv')

    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(comment_publisher_upvotes_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    if len(value) > 0 and downvoted:
        count = value[0]['count']
        count -= 1
        query = "UPDATE {} SET count = {} WHERE id_uniq = '{}' ;".format(comment_publisher_upvotes_table,  count, sender_id)
        cur.execute(query)
        print('checked !')
    elif len(value) == 0 :
        print('database error !')
    connection.commit()
    cur.close()
    return 

def comment_to_post(publisher_id, post_id, text):
    ''' all the input ids are uniqs '''
    try:
        cur=connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database while creating comment !")
        return
    
    # generating comment id at time of creation !
    code = helper.id_gen(cur, post_id, publisher_id, 'Comment')
    temp = ""
    for char in code :
        asc = ord(char)
        if (97 <= asc and asc <= 122) or (65 <= asc and asc <= 90):
            temp += char
    comment_id = temp


    query = "SELECT * FROM Id WHERE id_uniq = '{}' ;".format(comment_id)
    cur.execute(query)
    value = cur.fetchall();
    if len(value) == 0:
        # inserting this comment_id into Id table
        query = "INSERT INTO Id (id_obj, id_uniq) VALUES ('C', '{}') ;".format(comment_id)
        cur.execute(query)    

        # create required tables !
        query = "CREATE TABLE {}_{} (id_obj CHAR(1), id_uniq VARCHAR(200) NOT NULL UNIQUE, PRIMARY KEY (id_obj, id_uniq)) ;"
        table_list = ['upv', 'com', 'rep']
        for name in table_list:
            query1 = query.format(comment_id, name)
            print(query1, name)
            cur.execute(query1)

        # inserting this comment into Comment table as entry !
        query = "INSERT INTO Comment (id_uniq, author_obj, author_uniq, content, upvotes, comments, report_list, post_obj, post_uniq) VALUES ('{}', 'A', '{}', '{}', '{}_upv', '{}_com', '{}_rep', 'P', '{}');".format(comment_id, publisher_id, text, comment_id, comment_id, comment_id, post_id) # all default values are not given 
        cur.execute(query)

        # inserting comment_id into post's comment list
        query = "INSERT INTO {}_com (id_obj, id_uniq) VALUES ('C', '{}') ;".format(post_id, comment_id)
        cur.execute(query)
    else:
        print('already done !')
    print('commented to post !')
    connection.commit()
    cur.close()
    return 

def comment_to_comment(publisher_id, comment_id, text):
    ''' all the input ids are uniqs '''
    try:
        cur=connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database while creating comment on comment!")
        return
    
    # generating comment id at time of creation !
    code = helper.id_gen(cur, comment_id, publisher_id, 'Comment')
    temp = ""
    for char in code :
        asc = ord(char)
        if (97 <= asc and asc <= 122) or (65 <= asc and asc <= 90):
            temp += char
    comment_hash = temp

    print(comment_hash, 'hash')
    
    query = "SELECT * FROM Id WHERE id_uniq = '{}' ;".format(comment_hash)
    cur.execute(query)
    value = cur.fetchall();
    if len(value) == 0:
        # inserting this comment_hash into Id table
        query = "INSERT INTO Id (id_obj, id_uniq) VALUES ('C', '{}') ;".format(comment_hash)
        cur.execute(query)    

        # create required tables !
        query = "CREATE TABLE {}_{} (id_obj CHAR(1), id_uniq VARCHAR(200) NOT NULL UNIQUE, PRIMARY KEY (id_obj, id_uniq)) ;"
        table_list = ['upv', 'com', 'rep']
        for name in table_list:
            query1 = query.format(comment_hash, name)
            print(query1, name)
            cur.execute(query1)

        # inserting this comment into Comment table as entry !
        query = "INSERT INTO Comment (id_uniq, author_obj, author_uniq, content, upvotes, comments, report_list, post_obj, post_uniq) VALUES ('{}', 'A', '{}', '{}', '{}_upv', '{}_com', '{}_rep', 'P', '{}');".format(comment_hash, publisher_id, text, comment_hash, comment_hash, comment_hash, comment_id) # all default values are not given 
        cur.execute(query)
        
        # inserting comment_hash into comment's comment list
        query = "CREATE TABLE IF NOT EXISTS {}_com (id_obj CHAR(1), id_uniq VARCHAR(200), PRIMARY KEY (id_obj, id_uniq)) ;".format(comment_id)
        cur.execute(query)

        query = "INSERT INTO {}_com (id_obj, id_uniq) VALUES ('C', '{}') ;".format(comment_id, comment_hash)
        cur.execute(query)
    else:
        print('already done !')
    connection.commit()
    cur.close()
    return 


@app.route('/')
def start():
    try:
        cur=connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
        return
    print('start ')
    # follow(str("asdfgh12987"),str("asdfgh12345"))
    # follow(str("asdfgh12987"),str("asdfgh12345"))
    # unfollow(str("asdfgh12987"),str("asdfgh12345"))
    # unfollow(str("asdfgh12987"),str("asdfgh12345"))
    # upvote_for_post( "asdfgh12987", "mksdnq82910")
    # upvote_for_comment( "asdfgh12987", "asfnjk78495") # comment 
    # upvote_for_post( "asdfgh12987", "mksdnq82910")
    
    # downvote_for_post("asdfgh12987", "mksdnq82910")
    # downvote_for_comment("asdfgh12987", "asfnjk78495")
    # downvote_for_comment("asdfgh12987", "asfnjk78495")
    # downvote_for_comment("asdfgh12987", "asfnjk78495")
    # comment_to_post('asdfgh12987', 'mksdnq82910', '1st comment ')
    # comment_to_comment('asdfgh12987', "asfnjk78495", '1st comment to comment')
    print('end ')
    return render_template('html/start.html', message1="", message2="", show_forget=False)

@app.route('/js')
def start_js():
    return render_template('js/start.js')

@app.route('/js/main')
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

@app.route('/js/header/<string:user>')
def header_js(user):
    return render_template('js/header.js', user=user)

@app.route('/home/<string:username>')
def home(username):
    try:
        cur=connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
    query = "SELECT * from Account WHERE BINARY username = %s"
    cur.execute(query,(username,))
    user = cur.fetchall()[0]
    feed = helper.feed(cur, user)
    return render_template('html/home.html', user = user, feed = feed)

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
        cur=connection.cursor(MySQLdb.cursors.DictCursor)
    except:
        print("Can not connect to database in start page")
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
            cur=connection.cursor(MySQLdb.cursors.DictCursor)
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
                    otp_sub = str(otp[email])+" is your OTP for Synergy Login"
                    otp_body = otp_sub
                    helper.mail(email,otp_sub, otp_body)
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
            cur=connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in start page")
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
                    otp_signup[email] = helper.gen_otp()
                    otp_sub = str(otp_signup[email])+" is your OTP for Synergy Signup"
                    otp_body = "Hi "+username+"\nWelcome to Synergy,\n"+otp_sub
                    helper.mail(email,otp_sub, otp_body)
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
                        connection.commit()
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

def init_db():
    with app.app_context():
        try:
            cur=connection.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("Can not connect to database in init_db")
            return
        with app.open_resource('schema.sql', mode='r') as sql_file:
            cur.execute(sql_file.read())
        cur.close()
        connection.commit()
        sql_file.close()




if __name__ == "__main__":
    init_db()
    app.run(debug=True)