import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, import_data, sales_pub

sql_system = 'postgresql'
login = 'postgres'
password = 'Tdutybq2020'
name_db = 'book_shop_db'
host = '5432'

DSN = f'{sql_system}://{login}:{password}@localhost:{host}/{name_db}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
with open('tests_data.json') as f:
    data = json.load(f)

import_data(session, data)
publisher = input()
sales_pub(session, publisher)

session.close()