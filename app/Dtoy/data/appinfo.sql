CREATE TABLE appinfo (
    uid INTEGER NOT NULL PRIMARY KEY,
    appname VARCHAR (100) NOT NULL UNIQUE,
    apptype VARCHAR (20) NOT NULL,
    giturl VARCHAR (200) NOT NULL,
    branch VARCHAR (40) NOT NULL,
    typeinfo VARCHAR (40) NOT NULL ,
    submitter VARCHAR (40) NOT NULL,
    remarks VARCHAR (200) 
);