from re import search
from bcrypt import hashpw
from random import randint
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import b64encode
from datetime import datetime
from dateutil.relativedelta import relativedelta


def password_strength(password):
    length = len(password)
    if length < 4:
        return -1
    elif length < 8:
        if search('[a-z]', password) and search('[A-Z]', password) \
        and search('[0-9]', password):
            return 0
    else:
        if search('[a-z]', password) and search('[A-Z]', password) \
        and search('[0-9]', password) and search('[^a-zA-Z0-9]', password):
            return 1
    return 0

def hash_pwd(password):
    salt = b'$2b$12$BPgM2TZNwWMnrCl5d5Bjme'
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def gen_otp():
    otp=randint(100000,999999)
    return str(otp)

def mail( user_email, subject, msg ):
    mailll = str('synergyteam.dram@gmail.com')
    passss = str('yigympugyhpzznms')
    emaill = str(user_email)
    body = MIMEText(str(msg))
    SUBJECT = subject
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = "Synergy"
    msg['To'] = emaill
    msg.attach(body)
    s = SMTP(str('smtp.gmail.com'),587)
    s.starttls()
    s.login(mailll, passss)
    s.sendmail(mailll,[emaill], msg.as_string())
    s.quit()

def sql_to_list(data, key):
    key_list = []
    for entry in data:
        key_list.append(entry[key])
    return key_list

def feed(cur, user):
    tag_list = user['tag_list']
    query = 'SELECT * from {}'.format(tag_list)
    cur.execute(query)
    tag_list = cur.fetchall()
    if not tag_list:
        query = 'SELECT id_uniq from Tag'
        cur.execute(query)
        tag_list = cur.fetchall()
    tag_list = sql_to_list(tag_list,'id_uniq')
    post_dic = {}
    for tag_id in tag_list:
        query = "SELECT * from {}".format(tag_id+"_pos")
        cur.execute(query)
        post_list = cur.fetchall()
        post_list = sql_to_list(post_list, 'id_uniq')
        for post_id in post_list:
            if post_id in post_dic:
                post_dic[post_id]+=1
            else:
                post_dic[post_id] = 1
    num = 50    # number of posts in feed
    post_list_specific = sorted(post_dic, key=post_dic.get, reverse=True)
    count = 0
    feed = []   # stores (post_id, upvotes_count, already_upvoted, time_str, author_username,title, content, time, already_follow)
    for post_id in post_list_specific:
        if count == num:
            break
        query = "SELECT * from Post WHERE BINARY id_uniq = %s"
        cur.execute(query, (post_id,))
        post_data = cur.fetchall()[0]
        if post_data['public_post'] and post_data['visibility']:
            count += 1
            upvote_table = post_data['upvotes']
            query = "SELECT count(id_uniq) from {}".format(upvote_table)
            cur.execute(query)
            upvotes_count = cur.fetchall()[0]['count(id_uniq)']
            query = "SELECT * from {} WHERE BINARY id_uniq = %s".format(upvote_table)
            cur.execute(query, (user['id_uniq'],))
            already_upvoted = bool(cur.fetchall())
            time = relativedelta(datetime.now(),post_data['creation_time'])
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
            time = datetime.now() - post_data['creation_time']
            author_id = post_data['author_uniq']
            query = "SELECT username from Account WHERE BINARY id_uniq = %s"
            cur.execute(query, (author_id,))
            author_username = cur.fetchall()[0]['username']
            title = post_data['title']
            content = post_data['content']
            query = "SELECT * from {} WHERE BINARY id_uniq = %s".format(post_data['author_uniq']+"_ers")
            cur.execute(query, (user["id_uniq"],))
            already_follow = bool(cur.fetchall())
            feed.append((post_id, upvotes_count, int(already_upvoted), time_str, author_username, title, content, time, int(already_follow)))
    return feed

def check_username(username):
    if username:
        for i in username:
            if not (i.isalnum() or i=='_'):
                return False
        return True
    return False

def unique_username(cur, username):
    '''Return False if username already exists'''
    query = "SELECT username from Account WHERE BINARY username = %s"
    cur.execute(query, (username,))
    return not bool(cur.fetchall())

def id_gen(cur, id_obj, username, table):
    encoded_username = username[:9]
    if len(encoded_username)!=9:
        encoded_username = "x"*(9-len(encoded_username))+encoded_username
    query = "SELECT id_uniq FROM {} WHERE BINARY id_uniq LIKE '{}{}%' ORDER BY creation_time DESC LIMIT 1".format(table, id_obj, encoded_username)
    cur.execute(query)
    data = cur.fetchall()
    if data:
        id_uniq = data[0]['id_uniq']
        num = str(int(id_uniq[10:])+1).zfill(10)
    else:
        num = "0000000000"
    return id_obj+encoded_username+num

def create_linked_table(cur, id_uniq, suffix, ins_obj):
    if len(ins_obj)==1:
        query = "CREATE TABLE {} ( id_obj ENUM(%s) DEFAULT %s NOT NULL, id_uniq VARCHAR(200) NOT NULL UNIQUE, PRIMARY KEY (id_obj, id_uniq) )".format(id_uniq+suffix)
        cur.execute(query, (ins_obj,ins_obj))
    else:
        lst = list(ins_obj)
        obj_list = []
        for elem in lst:
            obj_list.append("'"+elem+"'")
        query = "CREATE TABLE {} (id_obj ENUM({}) NOT NULL, id_uniq VARCHAR(200) NOT NULL UNIQUE, PRIMARY KEY (id_obj, id_uniq))".format(id_uniq+suffix, ", ".join(obj_list))
        cur.execute(query)

def follow(cur, sender_id, profile_id):
    ''' inputs are the uniq values ! '''
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

def unfollow(cur, sender_id, profile_id):
    ''' Inputs values are id_uniq type !'''
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

def upvote_for_post(cur, sender_id, post_id):
    ''' requirements post_upvote_table, post_publisher_upvotes_table (obj, uniq, count = 0)'''
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
    return 

def upvote_for_comment(cur, sender_id, comment_id):
    '''requirements comments_upvote table, comment_publisher_upvote table (obj, uniq, count = 0)'''
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
    return 
    
def downvote_for_post(cur, sender_id, post_id):
    ''' requirements post_upvote_table, post_publisher_upvote_table '''
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
    return 

def downvote_for_comment(cur, sender_id, comment_id):
    ''' requirements comment_upvote_table, comment_publisher_upvote_table '''
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
    return 

def comment_to_post(cur, publisher_id, post_id, text):
    ''' all the input ids are uniqs '''
    
    # generating comment id at time of creation !
    code = id_gen(cur, post_id, publisher_id, 'Comment')
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
    return 

def comment_to_comment(cur, publisher_id, comment_id, text):
    ''' all the input ids are uniqs '''
    
    # generating comment id at time of creation !
    code = id_gen(cur, comment_id, publisher_id, 'Comment')
    temp = ""
    for char in code :
        asc = ord(char)
        if (97 <= asc and asc <= 122) or (65 <= asc and asc <= 90):
            temp += char
    comment_hash = temp

    print(comment_hash, 'hash')
    
    query = "SELECT * FROM Id WHERE id_uniq = '{}' ;".format(comment_hash)
    cur.execute(query)
    value = cur.fetchall()
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
    return