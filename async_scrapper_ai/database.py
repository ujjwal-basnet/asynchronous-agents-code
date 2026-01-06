from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import settings
from loguru import logger 

logger.info("extracting database url from settings")
DATABASE_URL= str(settings.pg_dsn)

logger.info("creating engine and session local")
engine= create_engine(DATABASE_URL , echo= False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

###### more database connection to dependencies ############ 

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()