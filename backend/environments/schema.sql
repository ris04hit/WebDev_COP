
-- check condition for the length of string where fixed length is needed !
-- last visit me on update wali cheej me mereko clarity nhi h !
-- abhi ke liye TEXT likh diye hai but usko as a tex file implement karna hai !
-- saare id_obj me NOT NULL bhi add karna hai kya ??
-- whereever get VARCHAR(100) means it is of set type thing and hence need to be stored in a different schema 


DROP DATABASE IF EXISTS Synergy_db;
Create DATABASE Synergy_db;

USE Synergy_db;

-- DROP SCHEMA IF EXISTS Base;
-- CREATE SCHEMA Base;

-- USE Base;

DROP TABLE IF EXISTS Account;
CREATE TABLE Account (
    id_obj CHAR(1) DEFAULT 'A',
    id_uniq VARCHAR(200) NOT NULL UNIQUE, 
    username VARCHAR(50) NOT NULL UNIQUE,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    name VARCHAR(150) NOT NULL,
    email_id VARCHAR(150) NOT NULL UNIQUE,
    institutes VARCHAR(100) NOT NULL UNIQUE, 
    posts INT DEFAULT 0,
    last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    upvotes VARCHAR(100) NOT NULL UNIQUE,
    -- profile_photo BLOB,  -- not certain of it tough
    bookmarks VARCHAR(100) NOT NULL UNIQUE,
    followers VARCHAR(100) NOT NULL UNIQUE,
    following VARCHAR(100) NOT NULL UNIQUE,
    comments VARCHAR(100) NOT NULL UNIQUE,
    visited_post VARCHAR(100) NOT NULL UNIQUE,
    activity VARCHAR(100) NOT NULL UNIQUE,
    tag_list VARCHAR(100) NOT NULL UNIQUE,
    country CHAR(150) ,
    state CHAR(150),
    city CHAR(150),
    website_address VARCHAR(1000),
    github_handle VARCHAR(150),
    organisation CHAR(150),
    visibility BOOLEAN DEFAULT true,
    report_list VARCHAR(100) NOT NULL UNIQUE,
    api_visibility BOOLEAN default true,
    PRIMARY KEY (id_obj, id_uniq)
);

DROP TABLE IF EXISTS Institution;
CREATE TABLE Institution (
    id_obj CHAR(1) DEFAULT 'I',
    id_uniq VARCHAR(200) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL UNIQUE,
    members VARCHAR(100) NOT NULL UNIQUE,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    posts VARCHAR(100) NOT NULL UNIQUE,
    description TEXT, -- needed to be tex file !
    -- domains VARCHAR(100) NOT NULL UNIQUE, -- what was this if anyone remembers ??
    admins VARCHAR(100) NOT NULL UNIQUE, 
    email_id VARCHAR(150) NOT NULL UNIQUE,
    visibility BOOLEAN DEFAULT true,
    api_visibility BOOLEAN DEFAULT true,
    PRIMARY KEY (id_obj, id_uniq)
);


DROP TABLE IF EXISTS Tag;
CREATE TABLE Tag (
    id_obj CHAR(1) DEFAULT 'T',
    id_uniq VARCHAR(200) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    posts VARCHAR(100) NOT NULL UNIQUE,
    members VARCHAR(100) NOT NULL UNIQUE,
    api_visibility BOOLEAN DEFAULT true,
    PRIMARY KEY (id_obj, id_uniq)
);

DROP TABLE IF EXISTS Id;
CREATE TABLE Id (
    id_obj CHAR(1) NOT NULL,
    id_uniq VARCHAR(200) NOT NULL UNIQUE,
    PRIMARY KEY (id_obj, id_uniq)
);


DROP TABLE IF EXISTS Post;
CREATE TABLE Post (
    id_obj CHAR(1) DEFAULT 'P',
    id_uniq VARCHAR(200) NOT NULL UNIQUE,
    author_obj CHAR(1),
    author_uniq VARCHAR(200),
    FOREIGN KEY (author_obj, author_uniq) REFERENCES Id(id_obj, id_uniq),
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    title TEXT,
    content TEXT, -- kuch karna h iska !! 
    upvotes VARCHAR(100) NOT NULL UNIQUE,
    comments VARCHAR(100) NOT NULL UNIQUE,
    report_list VARCHAR(100) NOT NULL UNIQUE,
    public_post BOOLEAN DEFAULT true,
    visibility BOOLEAN DEFAULT true,
    institutes VARCHAR(100)  NOT NULL UNIQUE,
    tag_list VARCHAR(100) NOT NULL UNIQUE,
    api_visibility BOOLEAN DEFAULT true,
    PRIMARY KEY (id_obj, id_uniq)
);

DROP TABLE IF EXISTS Comment;
CREATE TABLE Comment (
    id_obj CHAR(1) DEFAULT 'C',
    id_uniq VARCHAR(200) NOT NULL UNIQUE,
    author_obj CHAR(1),
    author_uniq VARCHAR(200),
    FOREIGN KEY (author_obj, author_uniq) REFERENCES Id(id_obj, id_uniq), 
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    content TEXT, -- isko change karna hai !
    upvotes VARCHAR(100) NOT NULL UNIQUE,
    comments VARCHAR(100) NOT NULL UNIQUE,
    report_list VARCHAR(100) NOT NULL UNIQUE,
    visibility BOOLEAN DEFAULT true,
    post_obj CHAR(1),
    post_uniq VARCHAR(200),
    FOREIGN KEY (post_obj, post_uniq) REFERENCES Id(id_obj, id_uniq),
    api_visibility BOOLEAN DEFAULT true,
    PRIMARY KEY (id_obj, id_uniq)
);

DROP TABLE IF EXISTS Report;
CREATE TABLE Report (
    id_obj CHAR(1) DEFAULT 'R',
    id_uniq VARCHAR(200) NOT NULL UNIQUE,
    from_obj CHAR(1),
    from_uniq VARCHAR(200),
    FOREIGN KEY (from_obj, from_uniq) REFERENCES Id(id_obj, id_uniq),
    to_obj CHAR(1),
    to_uniq VARCHAR(200),
    FOREIGN KEY (to_obj, to_uniq) REFERENCES Id(id_obj, id_uniq),
    description TEXT,
    api_visibility BOOLEAN DEFAULT true,
    PRIMARY KEY (id_obj, id_uniq)
);


-- DROP SCHEMA IF EXISTS Linked;
-- CREATE SCHEMA Linked;























-- -- Create a new table called "Account"

-- -- whereever get VARCHAR(100) means it is of set type thing and hence need to be stored in a different schema 
-- DROP TABLE IF EXISTS Account;

-- CREATE TABLE Account (
--     id_obj CHAR(1),
--     id_uniq VARCHAR(200), 
--     username VARCHAR(50),
--     creation_time DATETIME,
--     name VARCHAR(150),
--     email_id VARCHAR(150),
--     institutes VARCHAR(100),
--     posts INT,
--     last_visit DATETIME,
--     upvotes VARCHAR(100),
--     -- profile_photo BLOB,  -- not certain of it tough
--     bookmarks VARCHAR(100),
--     followers VARCHAR(100),
--     following VARCHAR(100),
--     comments VARCHAR(100),
--     visited_post VARCHAR(100),
--     activity VARCHAR(100),
--     tag_list VARCHAR(100),
--     country CHAR(150),
--     state CHAR(150),
--     city CHAR(150),
--     website_address VARCHAR(1000),
--     github_handle VARCHAR(150),
--     organisation CHAR(150),
--     visibility BOOLEAN,
--     report_list VARCHAR(100),
--     api_visibility BOOLEAN,
--     PRIMARY KEY (id_obj, id_uniq)
-- );

-- CREATE TABLE Institution (
--     id_obj CHAR(1),
--     id_uniq VARCHAR(200),
--     name VARCHAR(150),
--     members VARCHAR(100),
--     creation_time DATETIME,
--     posts VARCHAR(100),
--     description TEXT, -- needed to be tex file !
--     domains VARCHAR(100), -- what was this if anyone remembers ??
--     admins VARCHAR(100),
--     email_id VARCHAR(150),
--     visibility BOOLEAN,
--     api_visibility BOOLEAN,
--     PRIMARY KEY (id_obj, id_uniq)
-- );

-- CREATE TABLE Tag (
--     id_obj CHAR(1),
--     id_uniq VARCHAR(200),
--     name VARCHAR(150),
--     posts VARCHAR(100),
--     members VARCHAR(100),
--     api_visibility BOOLEAN,
--     PRIMARY KEY (id_obj, id_uniq)
-- );

-- CREATE TABLE Post (
--     id_obj CHAR(1),
--     id_uniq VARCHAR(200),
--     author_obj CHAR(1),
--     author_uniq VARCHAR(200),
--     FOREIGN KEY (author_obj, author_uniq) REFERENCES Account(id_obj, id_uniq),
--     creation_time DATETIME,
--     title TEXT,
--     content TEXT, -- kuch karna h iska !! 
--     upvotes VARCHAR(100),
--     comments VARCHAR(100),
--     report_list VARCHAR(100),
--     public_post BOOLEAN,
--     visibility BOOLEAN,
--     institutes VARCHAR(100),
--     tag_list VARCHAR(100),
--     api_visibility BOOLEAN,
--     PRIMARY KEY (id_obj, id_uniq)
-- );


-- CREATE TABLE Comment (
--     id_obj CHAR(1),
--     id_uniq VARCHAR(200),
--     author_obj CHAR(1),
--     author_uniq VARCHAR(200),
--     FOREIGN KEY (author_obj, author_uniq) REFERENCES Account(id_obj, id_uniq),
--     creation_time DATETIME,
--     content TEXT, --- isko change karna hai !
--     upvotes VARCHAR(100),
--     comments VARCHAR(100),
--     report_list VARCHAR(100),
--     visibility BOOLEAN,
--     post_obj CHAR(1),
--     post_uniq VARCHAR(200),
--     FOREIGN KEY (post_obj, post_uniq) REFERENCES Post(id_obj, id_uniq),
--     api_visibility BOOLEAN,
--     PRIMARY KEY (id_obj, id_uniq)
-- );


-- CREATE TABLE Report (
--     id_obj CHAR(1),
--     id_uniq VARCHAR(200),
--     author_obj CHAR(1),
--     author_uniq VARCHAR(200),
--     FOREIGN KEY (author_obj, author_uniq) REFERENCES Account(id_obj, id_uniq),
--     -- against_obj CHAR(1),
--     -- against_uniq VARCHAR(200),  -- how to handle ??
--     description TEXT,
--     api_visibility BOOLEAN,
--     PRIMARY KEY (id_obj, id_uniq)
-- ):