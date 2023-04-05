-- Create a new table called "Account"

-- whereever get VARCHAR(100) means it is of set type thing and hence need to be stored in a different schema 

CREATE TABLE Account (
    id_obj CHAR(1),
    id_uniq VARCHAR(200), 
    uesrname VARCHAR(50),
    creation_time DATETIME,
    name VARCHAR(150),
    email_id VARCHAR(150),
    institutes VARCHAR(100),
    posts INT,
    last_visit DATETIME,
    upvotes VARCHAR(100),
    -- profile_photo BLOB,  -- not certain of it tough
    bookmarks VARCHAR(100),
    followers VARCHAR(100),
    following VARCHAR(100),
    comments VARCHAR(100),
    visited_post VARCHAR(100),
    activity VARCHAR(100),
    tag_list VARCHAR(100),
    country CHAR(150),
    state CHAR(150),
    city CHAR(150),
    website_address VARCHAR(1000),
    github_handle VARCHAR(150),
    organisation CHAR(150),
    visibility BOOLEAN,
    report_list VARCHAR(100),
    api_visibility BOOLEAN,
    PRIMARY KEY (id_obj, id_uniq)
);

CREATE TABLE Institution (
    id_obj CHAR(1),
    id_uniq VARCHAR(200),
    name VARCHAR(150),
    members VARCHAR(100),
    creation_time DATETIME,
    posts VARCHAR(100),
    description TEXT, -- needed to be tex file !
    domains VARCHAR(100), -- what was this if anyone remembers ??
    admins VARCHAR(100),
    email_id VARCHAR(150),
    visibility BOOLEAN,
    api_visibility BOOLEAN,
    PRIMARY KEY (id_obj, id_uniq)
);

CREATE TABLE Tag (
    id_obj CHAR(1),
    id_uniq VARCHAR(200),
    name VARCHAR(150),
    posts VARCHAR(100),
    members VARCHAR(100),
    api_visibility BOOLEAN,
    PRIMARY KEY (id_obj, id_uniq)
);

CREATE TABLE Post (
    id_obj CHAR(1),
    id_uniq VARCHAR(200),
    author_obj CHAR(1),
    author_uniq VARCHAR(200),
    FOREIGN KEY (author_obj, author_uniq) REFERENCES Account(id_obj, id_uniq),
    creation_time DATETIME,
    title TEXT,
    content TEXT, -- kuch karna h iska !! 
    upvotes VARCHAR(100),
    comments VARCHAR(100),
    report_list VARCHAR(100),
    public_post BOOLEAN,
    visibility BOOLEAN,
    institutes VARCHAR(100),
    tag_list VARCHAR(100),
    api_visibility BOOLEAN,
    PRIMARY KEY (id_obj, id_uniq)
);


CREATE TABLE Comment (
    id_obj CHAR(1),
    id_uniq VARCHAR(200),
    author_obj CHAR(1),
    author_uniq VARCHAR(200),
    FOREIGN KEY (author_obj, author_uniq) REFERENCES Account(id_obj, id_uniq),
    creation_time DATETIME,
    content TEXT, --- isko change karna hai !
    upvotes VARCHAR(100),
    comments VARCHAR(100),
    report_list VARCHAR(100),
    visibility BOOLEAN,
    post_obj CHAR(1),
    post_uniq VARCHAR(200),
    FOREIGN KEY (post_obj, post_uniq) REFERENCES Post(id_obj, id_uniq),
    api_visibility BOOLEAN,
    PRIMARY KEY (id_obj, id_uniq)
);


CREATE TABLE Report (
    id_obj CHAR(1),
    id_uniq VARCHAR(200),
    author_obj CHAR(1),
    author_uniq VARCHAR(200),
    FOREIGN KEY (author_obj, author_uniq) REFERENCES Account(id_obj, id_uniq),
    -- against_obj CHAR(1),
    -- against_uniq VARCHAR(200),  -- how to handle ??
    description TEXT,
    api_visibility BOOLEAN,
    PRIMARY KEY (id_obj, id_uniq)
):