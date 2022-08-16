
CREATE TABLE IF NOT EXISTS Users (
    "id" INTEGER PRIMARY KEY NOT NULL,
    "firstname" TEXT NOT NULL,
    "lastname" TEXT NOT NULL,
    "username" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL
);