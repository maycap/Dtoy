CREATE TABLE "users" (
"uid"  INTEGER NOT NULL,
"nickname"  VARCHAR(100) NOT NULL,
"username"  VARCHAR(100) NOT NULL,
"identity"  VARCHAR(40) NOT NULL,
"email"  VARCHAR(120) NOT NULL,
"pwdhash"  VARCHAR(100) NOT NULL,
PRIMARY KEY ("uid" ASC),
UNIQUE ("email" ASC)
);

