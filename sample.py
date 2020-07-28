# root$ apt install --no-install-recommends libpq-dev postgresql postgresql-contrib
# root$ pip --no-cache-dir install psycopg2-binary sqlalchemy
# root$ service postgresql start (restart)
# root$ su postgres
# postgres$ psql
# postgres=# CREATE USER root WITH PASSWORD 'password' superuser;
# postgres=# \q
# postgres$ exit
# root$ psql postgres
# postgres=# CREATE DATABASE mydatabase;
# postgres=# \q
# root$ python sample.py

import json
import random
import pandas as pd

from sqlalchemy import create_engine

DATABASES = {
    'production':{
        'NAME': 'mydatabase',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '0.0.0.0',
        'PORT': 5432,
    },
}

db = DATABASES['production']

engine_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
    user = db['USER'],
    password = db['PASSWORD'],
    host = db['HOST'],
    port = db['PORT'],
    database = db['NAME'],
)

engine = create_engine(engine_string)
conn = engine.connect()

print("Opend database successfully")

conn.execute("""
    CREATE TABLE company (
        id       integer  PRIMARY KEY  NOT NULL,
        name     text                  NOT NULL,
        age      integer               NOT NULL,
        address  character (12),
        salary   real
    );
""")

conn.execute("""
    INSERT INTO company (id, name, age, address, salary)
    VALUES (1, 'Paul', 32, 'California', 20000.00);

    INSERT INTO company (id, name, age, address, salary)
    VALUES (2, 'Allen', 25, 'Texas', 15000.00);

    INSERT INTO company (id, name, age, address, salary)
    VALUES (3, 'Teddy', 23, 'Norway', 20000.00);

    INSERT INTO company (id, name, age, address, salary)
    VALUES (4, 'Mark', 25, 'Rich-Mond', 65000.00);
""")

conn.execute("""
    UPDATE company SET salary = %s WHERE id = %s;
""" %(str(25000.00), str(1)))

conn.execute("""
    DELETE FROM company WHERE id = 2;
""")

result = conn.execute("""
    SELECT id, name, address, salary FROM company;
""")
for row in result:
    print("id      = " + str(row[0]))
    print("name    = " + str(row[1]))
    print("address = " + str(row[2]))
    print("salary  = " + str(row[3]))

result = conn.execute("""
    SELECT id, name,  address, salary FROM company
        WHERE salary < (SELECT avg(salary) FROM company)
        AND salary > 20000;
""")
for row in result:
    print(row)

conn.execute("""
    DROP TABLE company;
""")

conn.execute("""
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
""")

for i in range(1, 6, 1):
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    result = conn.execute("""
        SELECT maximum(%s, %s);
    """ %(str(a), str(b)))
    for row in result:
        print(str(i) + ". maximum(" + str(a) + ", " + str(b) + ") = " + str(row[0]))

conn.execute("""
    DROP FUNCTION maximum;
""")

df = pd.read_csv("item.csv")
print(df)

df.to_sql('item', engine, if_exists='append', index=False)

result = conn.execute("""
    SELECT * FROM item;
""")
for row in result:
    print("name  = " + str(row[0]))
    print("price = " + str(row[1]))

# postgresql -> pandas
df = pd.read_sql_table('item', engine)
print(df)

conn.execute("""
    DROP TABLE item;
""")

conn.execute("""
    CREATE TABLE company (
        id    bigserial  PRIMARY KEY,
        data  jsonb
    );
""")

conn.execute("""
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
                "2018": "Project Engineer",
                "2019": "Senior Project Engineer"
            }
    }');
""")

result = conn.execute("""
    SELECT id, jsonb_pretty(data) FROM company WHERE (data ->> 'age')::integer = 32;
""")
for row in result:
    print(row[1])
    print("name    = " + str(json.loads(row[1])["name"]))
    print("age     = " + str(json.loads(row[1])["age"]))
    print("address = " + str(json.loads(row[1])["address"]))
    print("salary  = " + str(json.loads(row[1])["salary"]))
    print("title   = " + str(json.loads(row[1])["title"]))

conn.execute("""
    DROP TABLE company;
""")

conn.close()
