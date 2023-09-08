import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables

DSN = 'postgresql://postgres:Tdutybq2020@localhost:5432/book_shop_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.close()