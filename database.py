"""
this file for creating database instance for crud operations in databse. it connects to database
"""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:pgadmin1234@localhost/Quiz2", echo=True)
Base = declarative_base()
Session_local = sessionmaker(bind=engine)
