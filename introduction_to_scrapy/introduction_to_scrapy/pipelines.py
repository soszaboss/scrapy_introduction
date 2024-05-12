# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from introduction_to_scrapy.models import Base, Book
from sqlalchemy.orm import Session
class IntroductionToScrapyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            adapter['price'] = float(adapter['price'].replace('£', ''))
        if adapter.get('avaibility'):
            adapter['avaibility'] = int(adapter['avaibility'].split('(')[1].split(" ")[0])
        if adapter.get('description'):
            adapter['description'] = adapter['description'].strip()
        return item


class SaveToPostgresSql():
    def __init__(self) -> None:
        self.URL = "postgresql+psycopg://postgres:OxyContin@localhost:5432/books"
        self.create_all()


    def engine(self):
        return create_engine(self.URL)
    

    def create_all(self):
        connection = self.engine().connect()
        if not self.engine().dialect.has_table(connection=connection, table_name="books"):
            engine = self.engine()
            return Base.metadata.create_all(engine)
        
    @staticmethod
    def book(func):
        def session(*args, **kwargs):
            engine = create_engine("postgresql+psycopg://postgres:OxyContin@localhost:5432/books")
            with Session(engine) as session:
                book_data = func(*args, **kwargs)
                session.add(book_data)
                session.commit()
                print("bon")
        return session


    @book
    def book_items(self, title:str, price:float, description:str, upc:str, avaibility:int):
        return Book(title=title, price=price, description=description, upc=upc, avaibility=avaibility)


    def process_item(self, item, spider):
        title= item['title']
        price= item['price']
        description= item['description']
        upc= item['upc']
        avaibility= item['avaibility']
        self.book_items(title, price, description, upc, avaibility)
        return item

class SaveToMongoDB():
    pass