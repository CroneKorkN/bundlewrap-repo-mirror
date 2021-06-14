DROP TABLE users; DROP TABLE domains;

CREATE TABLE domains (
  "id" BIGSERIAL PRIMARY KEY,
  "name" varchar(255) UNIQUE NOT NULL
);
CREATE INDEX ON domains ("name");

CREATE TABLE users (
  "id" BIGSERIAL PRIMARY KEY,
  "name" varchar(255) NOT NULL,
  "domain_id" BIGSERIAL NOT NULL,
  CONSTRAINT "fk_domain"
    FOREIGN KEY("domain_id") 
      REFERENCES domains("id"),
  "password" varchar(255) NOT NULL,
  "redirect" varchar(255) DEFAULT NULL
);
CREATE UNIQUE INDEX ON users ("name", "domain_id") WHERE "redirect" IS NULL;
