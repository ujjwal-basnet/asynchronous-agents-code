from fastapi import Body
from loguru import logger 
from typing import Generator 
from schemas import TextModelRequest, TextModelResponse
from scrapper import extract_urls, fetch_all
from database import SessionLocal 
from sqlalchemy.orm import Session
from uuid import uuid4 

##################################### database session ####################### 
def get_db()-> Generator[Session, None , None ]: 
    db = SessionLocal()  ### our database is now  session object
    try :
        yield db 

    finally : 
        db.close() 

    
# ------------------- URL content  -------------------
async def get_urls_content(
    body: TextModelRequest= Body(...),  ), -> str : 

    logger.info("extract urls")
    urls= extract_urls(body.prompts)
    # -------------------async  scraping  ----------------------------- 
    try :  
        urls_contents= await fetch_all(urls) # async scrapping  ## result is .join (string) so no worries
        return urls_contents
    
    except as e: 
        logger.warning("error on fetching {e}")
        return " "


    


