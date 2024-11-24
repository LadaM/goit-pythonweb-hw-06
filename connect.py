from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

url_to_db = "postgresql://lada:42snails@localhost:5432/postgres"

engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()