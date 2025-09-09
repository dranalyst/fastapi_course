from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://todoappdb_xkjl_user:zFLvDaOwk1mQEO3gl4IsoxGUJHPV4pmq@dpg-d306eh75r7bs73b30tbg-a.frankfurt-postgres.render.com/todoappdb_xkjl'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:c6emcpostgres@localhost/todoApplicationDatabase'
#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root@127.0.0.1:3306/todoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()