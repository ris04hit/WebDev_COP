from re import search
from bcrypt import hashpw
from random import randint
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import b64encode
from datetime import datetime
from dateutil.relativedelta import relativedelta
from random import randint


def password_strength(password):
    length = len(password)
    if length < 8:
        return -1
    elif length < 12:
        if search('[a-z]', password) and search('[A-Z]', password) \
        and search('[0-9]', password):
            return 1
    else:
        if search('[a-z]', password) and search('[A-Z]', password) \
        and search('[0-9]', password) and search('[^a-zA-Z0-9]', password):
            return 1
    return 1

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
    print(tag_list)
    tag_list = list(cur.fetchall())
    print(tag_list)
    if len(tag_list)<50:
        query = 'SELECT id_uniq from Tag'
        cur.execute(query)
        tag_list.extend(list((cur.fetchall())[:50-len(tag_list)]))
    tag_list = sql_to_list(tag_list,'id_uniq')
    print(tag_list)
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
    encoded_username = username[1:9]
    if len(encoded_username)!=9:
        encoded_username = id_obj+"x"*(9-len(encoded_username))+encoded_username
    if table != 'Tag':
        query = "SELECT id_uniq FROM {} WHERE BINARY id_uniq LIKE '{}{}%' ORDER BY creation_time DESC LIMIT 1;".format(table, id_obj, encoded_username)
        cur.execute(query)
        data = cur.fetchall()
    else:
        query = "Select id_uniq from {} ORDER BY id_uniq ;".format(table)
        cur.execute(query)
        data = cur.fetchall()
    num = randint(0,9999999999)
    # if data:
    #     id_uniq = data[-1]['id_uniq']
    #     num = str(int(id_uniq[10:])+1).zfill(10)
    # else:
    #     num = "0000000000"
    return id_obj+encoded_username+str(num)

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

# def follow(cur, sender_id, profile_id):
#     ''' inputs are the uniq values ! '''
#     profile_followers = profile_id + str('_ers')
#     sender_following = sender_id + str('_ing')
#     query = ("SELECT * from {} WHERE id_uniq= '{}' ;".format(profile_followers, sender_id))
#     cur.execute(query)
#     value = cur.fetchall()
#     if len(value) == 0 :
#         query = ("INSERT INTO {} (id_obj, id_uniq) VALUES ( '{}', '{}');".format(profile_followers, 'A', sender_id))
#         cur.execute(query)
#         # insert into the following list !
#         query = "SELECT * from {} WHERE id_uniq= '{}' ;".format(sender_following, profile_id)
#         cur.execute(query)
#         value = cur.fetchall()
#         if len(value) == 0 :
#             query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('{}', '{}');".format(sender_following, 'A', profile_id)
#             cur.execute(query)
#         else:
#             print('#'*20 + '\n   DATABASE IS CORRUPTED !!\n')
#     else:
#         uniq = profile_id
#         query = "SELECT name FROM Account WHERE id_uniq = '{}' ;".format(uniq)
#         cur.execute(query)
#         account_name = cur.fetchall()
#         print('You have already followed {}'.format(account_name[0]['name']))

# def unfollow(cur, sender_id, profile_id):
#     ''' Inputs values are id_uniq type !'''
#     # following from mani's ac to mecan's ac
#     sender_following = sender_id + str('_ing')
#     profile_followers = profile_id + str('_ers')
#     query = ("SELECT * from {} WHERE id_uniq= '{}' ;".format(profile_followers, sender_id))
#     cur.execute(query)
#     value = cur.fetchall()
#     # print('val', value)
#     if len(value) > 0 :
#         query = "DELETE FROM {} WHERE id_uniq = '{}';".format(profile_followers, value[0]['id_uniq'])
#         cur.execute(query)
#         # deleting from the following list !
#         query = ("SELECT * from {} WHERE id_uniq= '{}' ;".format(sender_following, profile_id))
#         cur.execute(query)
#         value = cur.fetchall()
#         if len(value) > 0:
#             query = "DELETE FROM {} WHERE id_uniq = '{}';".format(sender_following, value[0]['id_uniq'])
#             cur.execute(query)
#         else:
#             print('#'*20 + '\n   DATABASE IS CORRUPTED !!\n')
#     else:
#         query = "SELECT name FROM Account WHERE id_uniq = '{}' ;".format(profile_id)
#         cur.execute(query)
#         account_name = cur.fetchall()
#         print("Already unfollowed {}".format(account_name[0]['name']))

def upvote_for_post_help(cur, sender_id, post_id):
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

# def upvote_for_comment(cur, sender_id, comment_id):
#     '''requirements comments_upvote table, comment_publisher_upvote table (obj, uniq, count = 0)'''
#     comment_upvote_table = comment_id + str('_upv')
#     query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(comment_upvote_table, sender_id)
#     cur.execute(query)
#     value = cur.fetchall()
#     upvoted = False
#     if len(value) == 0:
#         query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('A', '{}') ;".format(comment_upvote_table, sender_id)
#         cur.execute(query)
#         print('upvoted to coomment')
#         upvoted = True
#     else :
#         print('already upvoted to comment')
#         return 
    
#     query = "SELECT author_uniq FROM Comment WHERE id_uniq = '{}' ;".format(comment_id)
#     cur.execute(query)
#     value = cur.fetchall()
#     comment_publisher_id = value[0]['author_uniq']
#     comment_publisher_upvotes_table = comment_publisher_id + str('_upv')

#     query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(comment_publisher_upvotes_table, sender_id)
#     cur.execute(query)
#     value = cur.fetchall()
#     if len(value) == 0 :
#         query = "INSERT INTO {} (id_obj, id_uniq, count) VALUES ('A', '{}', 1) ;".format(comment_publisher_upvotes_table, sender_id)
#         cur.execute(query)
#     elif upvoted:
#         count = value[0]['count']
#         count += 1
#         query = "UPDATE {} SET count = {} WHERE id_uniq = '{}' ;".format(comment_publisher_upvotes_table,  count, sender_id)
#         cur.execute(query)
#         print('checked !')
#     return 


def upvote_for_post_help(cur, sender_id, post_id):
    ''' requirements post_upvote_table, post_publisher_upvotes_table (obj, uniq, count = 0)'''
    post_upvote_table = post_id + str('_upv')
    query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(post_upvote_table, sender_id)
    cur.execute(query)
    value = cur.fetchall()
    upvoted = False
    if len(value) == 0:
        query = "INSERT INTO {} (id_obj, id_uniq) VALUES ('A', '{}') ;".format(post_upvote_table, sender_id)
        cur.execute(query)
        # mysql.connection.commit()
        print('upvoted to post from function')
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
        # mysql.connection.commit()
    elif upvoted:
        count = value[0]['count']
        count += 1
        query = "UPDATE {} SET count = {} WHERE id_uniq = '{}' ;".format(post_publisher_upvotes_table,  count, sender_id)
        cur.execute(query)
        print('checked !')
    # mysql.connection.commit()
    return 

    
# def downvote_for_post_help(cur, sender_id, post_id):
#     ''' requirements post_upvote_table, post_publisher_upvote_table '''
#     post_upvote_table = post_id + str('_upv')
#     query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(post_upvote_table, sender_id)
#     cur.execute(query)
#     value = cur.fetchall()
#     downvoted = False
#     if len(value) > 0:
#         query = "DELETE FROM {} WHERE id_uniq = '{}' ;".format(post_upvote_table, sender_id)
#         cur.execute(query)
#         print('downvoted post')
#         downvoted = True
#     else:
#         print('already downvoted to post !')
#         return 
    
#     # finding post_publisher_id 
#     query = "SELECT author_uniq FROM Post WHERE id_uniq = '{}' ;".format(post_id)

#     cur.execute(query)
#     value = cur.fetchall()
#     post_publisher_id = value[0]['author_uniq']
#     post_publisher_upvotes_table = post_publisher_id + str('_upv')

#     query = "SELECT * FROM {} WHERE id_uniq = '{}' ;".format(post_publisher_upvotes_table, sender_id)
#     cur.execute(query)
#     value = cur.fetchall()
#     if len(value) > 0 and downvoted:
#         count = value[0]['count']
#         count -= 1
#         query = "UPDATE {} SET count = {} WHERE id_uniq = '{}' ;".format(post_publisher_upvotes_table,  count, sender_id)
#         cur.execute(query)
#         print('checked !')
#     elif len(value) == 0 :
#         print('database error !')
#     return 




def downvote_for_post_help(cur, sender_id, post_id):
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


def comment_get (cur, comment_id):
    query = "SELECT * FROM Comment WHERE id_uniq = '{}' ;".format(comment_id['id_uniq'])
    print("\n\n",query,"\n\n")
    cur.execute(query)
    comment_list = cur.fetchall()
    return_list = []
    for comment in comment_list:
        print("\n\n\n 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ",comment,"\n\n\n")
        author = comment['author_uniq']
        query = "SELECT * FROM Account WHERE id_uniq = '{}' ;".format(author)
        cur.execute(query)
        author = cur.fetchall()[0]
        comment['author_name'] = author['username']
        creation_time = comment['creation_time']
        time = relativedelta(datetime.now(),creation_time)
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
        comment['creation_time'] = time_str
        comment_table = comment['comments']
        query = "SELECT * FROM {} ;".format(comment_table)
        cur.execute(query)
        comment_list = cur.fetchall()
        comment['comment_list'] = []
        for commentnest in comment_list:
            comment['comment_list'].append(comment_get(cur, commentnest))
    print("\nHelloriz\n",comment)
    return return_list


def follow_help(cur, sender_id, profile_id):
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

def unfollow_help(cur, sender_id, profile_id):
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

def profile_data(cur, username, curr_user):
    query = "SELECT * from Account WHERE username = %s"
    cur.execute(query, (username,))
    profile = cur.fetchall()[0]
    query = "SELECT * from {} WHERE id_uniq = %s".format(profile['followers'])
    cur.execute(query, (curr_user['id_uniq'],))
    profile['isfollow'] = bool(cur.fetchall())
    profile['membersince'] = str(profile['creation_time'].month)+"/"+str(profile['creation_time'].year)[2:]
    query = "SELECT * from {}".format(profile['upvotes'])
    cur.execute(query)
    profile['count'] = len(cur.fetchall())
    query = "SELECT * from {}".format(profile['institutes'])
    cur.execute(query)
    insti = cur.fetchall()
    insti_list = []
    for institution in insti:
        query = "SELECT name, id_uniq from Institution WHERE id_uniq = %s"
        cur.execute(query, (institution['id_uniq'],))
        insti_list.append(cur.fetchall()[0])
    profile['insti_list'] = insti_list
    query = "SELECT * from {}".format(profile['followers'])
    cur.execute(query)
    followers = cur.fetchall()
    follower_list = []
    for follower in followers:
        query = "SELECT username, id_uniq from Account WHERE id_uniq = %s"
        cur.execute(query, (follower['id_uniq'],))
        follower_list.append(cur.fetchall()[0])
    profile['follower_list'] = follower_list
    query = "SELECT * from {}".format(profile['following'])
    cur.execute(query)
    following_all = cur.fetchall()
    following_list = []
    for following in following_all:
        query = "SELECT username, id_uniq from Account WHERE id_uniq = %s"
        cur.execute(query, (following['id_uniq'],))
        following_list.append(cur.fetchall()[0])
    profile['following_list'] = following_list
    query = "SELECT * from {}".format(profile['tag_list'])
    cur.execute(query)
    tags = cur.fetchall()
    tag_list = []
    for tag in tags:
        query = "SELECT name, id_uniq from Tag WHERE id_uniq = %s"
        cur.execute(query, (tag['id_uniq'],))
        tag_list.append(cur.fetchall()[0])
    profile['tag_list'] = tag_list
    query = "SELECT * from {}".format(profile['posts'])
    cur.execute(query)
    post_list_specific = cur.fetchall()
    print("yolisst",post_list_specific)
    feed = []   # stores (post_id, upvotes_count, already_upvoted, time_str, author_username,title, content, time, already_follow)
    num = 50
    count = 0
    for post_id in post_list_specific:
        if count == num:
            break
        post_id = post_id['id_uniq']
        query = "SELECT * from Post WHERE BINARY id_uniq = %s"
        cur.execute(query, (post_id,))
        post_data = cur.fetchall()[0]
        if post_data['public_post'] and post_data['visibility']:
            print(0)
            count += 1
            upvote_table = post_data['upvotes']
            query = "SELECT count(id_uniq) from {}".format(upvote_table)
            cur.execute(query)
            upvotes_count = cur.fetchall()[0]['count(id_uniq)']
            query = "SELECT * from {} WHERE BINARY id_uniq = %s".format(upvote_table)
            cur.execute(query, (curr_user['id_uniq'],))
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
            cur.execute(query, (curr_user["id_uniq"],))
            already_follow = bool(cur.fetchall())
            feed.append((post_id, upvotes_count, int(already_upvoted), time_str, author_username, title, content, time, int(already_follow)))
    return profile, feed

def institute_data(cur, inst_id, curr_user):
    query = "SELECT * from Institution WHERE BINARY id_uniq = %s"
    cur.execute(query, (inst_id,))
    insti_data = cur.fetchall()[0]
    members = []
    top_contributor = {}
    query = "SELECT * from Account"
    cur.execute(query)
    users = cur.fetchall()
    for user in users:
        query = "SELECT * from {}".format(user['institutes'])
        cur.execute(query)
        user_insti = cur.fetchall()
        flag = False
        for i in user_insti:
            if inst_id == i['id_uniq']:
                flag = True
                break
        if flag:
            members.append(user['username'])
    insti_data['members'] = members
    insti_data['isfollow'] = curr_user['username'] in members
    insti_data['membersince'] = str(insti_data['creation_time'].month)+"/"+str(insti_data['creation_time'].year)[2:]
    query = "SELECT * from Account WHERE BINARY id_uniq = %s"
    cur.execute(query, (insti_data['admin_uniq'],))
    insti_data['admin_username'] = cur.fetchall()[0]['username']
    query = "SELECT * from Post"
    cur.execute(query)
    post_list_specific = []
    post_data = cur.fetchall()
    for post_item in post_data:
        query = 'SELECT * from {}'.format(post_item['institutes'])
        cur.execute(query)
        post_insti = cur.fetchall()
        flag = False
        for i in post_insti:
            if inst_id == i['id_uniq']:
                flag = True
                break
        if flag:
            post_list_specific.append(post_item['id_uniq'])
            if post_item['author_uniq'] in top_contributor:
                top_contributor[post_item['author_uniq']] += 1
            else:
                top_contributor[post_item['author_uniq']] = 1
    top_list = []
    for author_id in top_contributor:
        query = "SELECT * from Account WHERE id_uniq = %s"
        cur.execute(query, (author_id,))
        author_data = cur.fetchall()[0]
        top_list.append((top_contributor[author_id], author_data['username']))
    insti_data['top_contributor'] = top_list[:10]
    feed = []   # stores (post_id, upvotes_count, already_upvoted, time_str, author_username,title, content, time, already_follow, author_id)
    num = 50
    count = 0
    for post_id in post_list_specific:
        if count == num:
            break
        query = "SELECT * from Post WHERE BINARY id_uniq = %s"
        cur.execute(query, (post_id,))
        post_data = cur.fetchall()[0]
        if post_data['public_post'] and post_data['visibility']:
            print(0)
            count += 1
            upvote_table = post_data['upvotes']
            query = "SELECT count(id_uniq) from {}".format(upvote_table)
            cur.execute(query)
            upvotes_count = cur.fetchall()[0]['count(id_uniq)']
            query = "SELECT * from {} WHERE BINARY id_uniq = %s".format(upvote_table)
            cur.execute(query, (curr_user['id_uniq'],))
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
            cur.execute(query, (curr_user["id_uniq"],))
            already_follow = bool(cur.fetchall())
            feed.append((post_id, upvotes_count, int(already_upvoted), time_str, author_username, title, content, time, int(already_follow), author_id))
    return insti_data, feed

def find_contribution_individual(cur, user_id):
    '''Returns the number of posts posted by a user'''
    query = "SELECT * from Account WHERE BINARY id_uniq = '{}';".format(user_id)
    # print(query)
    cur.execute(query)
    value = cur.fetchall()
    # print(value)
    if value:
        value = value[0]
        contribution = value['posts']
        query = "select * from {} ;".format(contribution)
        cur.execute(query)
        ans = cur.fetchall()
        # print(ans)
        return len(ans)
    return 0

def contribution_user(cur):
    '''Returns the number of posts posted by all users'''
    data = []
    query = "SELECT * from Account ;"
    cur.execute(query)
    value = cur.fetchall()
    # print('value\n'*20 ,value)

    for sets in value:
        data.append((find_contribution_individual(cur, sets['id_uniq']), sets['username'], sets['id_uniq']))
    
    data.sort(reverse=True)
    # print(data )
    return data[:5]

def contribution_inst(cur):
    '''Returns the number of posts posted by all institutions'''
    data = []
    query = "SELECT * from Institution ;"
    cur.execute(query)
    Institutions = cur.fetchall()

    for sets in Institutions:
        member_list = sets['members']
        query = "SELECT * from {} ;".format(member_list)
        cur.execute(query)
        members = cur.fetchall()
        ans1 = 0
        for member in members:
            ans1 += find_contribution_individual(cur, member['id_uniq'])

        query = "SELECT * from {};".format(sets['posts'])
        cur.execute(query)
        ans2 = len(cur.fetchall())
        data.append((ans1 + ans2, sets['name'], sets['id_uniq']))

        # ans1 = sum of posts from members in that institution
        # ans2 = total post posted in that institution
    
    data.sort(reverse=True)
    # print(data)
    return data[:5]
    

def find_likes_post(cur, post_id):
    '''Returns the number of likes on a post'''
    query = "SELECT * FROM {}_upv;".format(post_id)
    cur.execute(query)
    upvotes = cur.fetchall()
    return len(upvotes)

def find_likes_user(cur, user_id):
    '''Returns the number of likes on all posts of a user'''
    query = "SELECT * from Account WHERE BINARY id_uniq = '{}';".format(user_id)
    cur.execute(query)
    value = cur.fetchall()
    if value:
        value = value[0]
        posts = value['posts']
        query = "select * from {} ;".format(posts)
        cur.execute(query)
        ans = cur.fetchall()
        likes = 0
        for post in ans:
            likes += find_likes_post(cur, post['id_uniq'])
        return likes
    return 0

def likes_user(cur):
    '''Returns the number of likes on all posts of all users'''
    data = []
    query = "SELECT * from Account ;"
    cur.execute(query)
    users = cur.fetchall()
    for acc in users:
        data.append((find_likes_user(cur, acc['id_uniq']), acc['username'], acc['id_uniq'])) 
    data.sort(reverse=True)
    # print(data)
    return data[:5]       
    

def likes_inst(cur):
    '''Returns the number of likes on all posts of all institutions : ans2'''
    data = []
    query = "SELECT * from Institution ;"
    cur.execute(query)
    Institutions = cur.fetchall()
    for insti in Institutions:
        members = insti['members']
        query = "SELECT * from {} ;".format(members)
        cur.execute(query)
        members = cur.fetchall()
        ans1 = 0
        for member in members:
            ans1 += find_likes_user(cur, member['id_uniq'])
        
        query = "SELECT * from {};".format(insti['posts'])
        cur.execute(query)
        posts = cur.fetchall()
        ans2 = 0
        for post in posts:
            ans2 += find_likes_post(cur, post['id_uniq'])
        data.append((ans2, insti['name'], insti['id_uniq']))
    data.sort(reverse=True)
    print(data)
    return data[:5]