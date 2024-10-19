CREATE TABLE "contacts" (
  "id" serial PRIMARY KEY,
  "fullname" varchar(255) NOT NULL,
  "phone_number" varchar(30) NOT NULL,
  "user_id" int
);

CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "fullname" varchar(255) NOT NULL,
  "email" varchar(100) UNIQUE NOT NULL,
  "hashed_password" varchar(255) NOT NULL
);

ALTER TABLE "contacts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
