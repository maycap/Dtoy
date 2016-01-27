CREATE TABLE deploylog (
    id INTEGER NOT NULL PRIMARY KEY,
    appname VARCHAR (50) NOT NULL ,
    user VARCHAR (50) NOT NULL,
    status VARCHAR (100) NOT NULL,
    submit_time DATETIME  NOT NULL
);