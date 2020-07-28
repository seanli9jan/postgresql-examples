-- root$ apt install --no-install-recommends postgresql postgresql-contrib
-- root$ service postgresql start (restart)
-- root$ su postgres
-- postgres$ psql
-- postgres=# CREATE USER root WITH PASSWORD 'password' superuser;
-- postgres=# \q
-- postgres$ exit
-- root$ psql postgres
-- postgres=# CREATE DATABASE mydatabase;
-- postgres=# \q
-- root$ PGPASSWORD=password psql -d mydatabase -U root -h 0.0.0.0 -p 5432 -E -w -f sample.sql

CREATE TABLE company (
    id       integer  PRIMARY KEY  NOT NULL,
    name     text                  NOT NULL,
    age      integer               NOT NULL,
    address  character (12),
    salary   real
);

INSERT INTO company (id, name, age, address, salary)
VALUES (1, 'Paul', 32, 'California', 20000.00);

INSERT INTO company (id, name, age, address, salary)
VALUES (2, 'Allen', 25, 'Texas', 15000.00);

INSERT INTO company (id, name, age, address, salary)
VALUES (3, 'Teddy', 23, 'Norway', 20000.00);

INSERT INTO company (id, name, age, address, salary)
VALUES (4, 'Mark', 25, 'Rich-Mond', 65000.00);

UPDATE company SET salary = 25000.00 WHERE id = 1;

DELETE FROM company WHERE id = 2;

SELECT id, name, address, salary FROM company;

DROP TABLE company;

CREATE FUNCTION maximum (a integer, b integer)
RETURNS integer AS $$
BEGIN
    IF (a > b) THEN
        RETURN a;
    ELSE
        RETURN b;
    END IF;
END;
$$ LANGUAGE plpgsql;
--SELECT maximum(2, 3);

DO $$
DECLARE
    i integer := 5;
    a integer;
    b integer;
BEGIN
    FOR counter IN 1..i LOOP
        a := floor(random() * 10)::integer;
        b := floor(random() * 10)::integer;
        RAISE NOTICE '%. maximum(%, %) = %', counter, a, b, maximum(a, b);
    END LOOP;
END; $$;

DROP FUNCTION maximum;

CREATE TABLE item (
    name   text  PRIMARY KEY  NOT NULL,
    price  real               NOT NULL
);

\COPY item FROM 'item.csv' DELIMITER ',' CSV HEADER;

SELECT * FROM item;

DROP TABLE item;

CREATE TABLE company (
    id    bigserial  PRIMARY KEY,
    data  jsonb
);

INSERT INTO company (data)
VALUES ('{
        "name": "Paul",
        "age": 32,
        "address": "California",
        "salary": 20000.00,
        "title": {
            "2017": "Project Engineer",
            "2018": "Senior Project Engineer",
            "2019": "RD Supervisor"
        }
}'), ('{
        "name": "Allen",
        "age": 25,
        "address": "Texas",
        "salary": 15000.00,
        "title": {
            "2016": "Project Engineer",
            "2017": "Project Engineer",
            "2018": "Project Engineer"
        }
}');

SELECT id, jsonb_pretty(data) FROM company WHERE (data ->> 'age')::integer = 32;

DROP TABLE company;
