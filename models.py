import sqlalchemy as sq
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True, nullable=False)

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True, nullable=False)

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    CheckConstraint('count > 0', name='count_check')
    shops = relationship(Shop, backref='stocks')
    books = relationship(Book, backref='books')

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    CheckConstraint('price > 0', name='price_check')
    CheckConstraint('count > 0', name='count_check')
    stock = relationship(Stock, backref='stocks')

def import_data(session, data: list):
    for row in data:
        if row['model'] == 'publisher':
            publisher = Publisher(name=row['fields']['name'])
            session.add(publisher)
        elif row['model'] == 'book':
            book = Book(title=row['fields']['title'], id_publisher=row['fields']['id_publisher'])
            session.add(book)
        elif row['model'] == 'shop':
            shop = Shop(name=row['fields']['name'])
            session.add(shop)
        elif row['model'] == 'stock':
            stock = Stock(id_shop=row['fields']['id_shop'],
                          id_book=row['fields']['id_book'], count=row['fields']['count'])
            session.add(stock)
        elif row['model'] == 'sale':
            sale = Sale(price=row['fields']['price'], date_sale=row['fields']['date_sale'],
                        count=row['fields']['count'], id_stock=row['fields']['id_stock'])
            session.add(sale)
        session.commit()

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def sales_pub(session, row: str):
    book = session.query(Publisher.name, Publisher.id, Book.title, Shop.name, (Sale.count * Sale.price),
                         Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)

    if row.strip().isdigit():
        lines = book.filter(Publisher.id == int(row.strip())).all()
    else:
        lines = book.filter(Publisher.name == row.strip()).all()
    row = ''

    for line in lines:
        row += line[2] + ' | '
        row += line[3] + ' | '
        row += str(line[4]) + ' | '
        row += str(line[5])
        print(row)

