from sqlalchemy import create_engine, MetaData, Table

metadata_obj = MetaData()

engine = create_engine('sqlite:///test.db', echo=True)
