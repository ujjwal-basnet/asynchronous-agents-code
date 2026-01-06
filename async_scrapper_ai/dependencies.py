from fastapi import Body
from loguru import logger 
from schemas import TextModelRequest
from scrapper import extract_urls, fetch_all
from database import SessionLocal 


# --------------------- open database as dependency -----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# -------------------  Injecting WebScrapping functionality as dependency in  Fastapi LLM  controller  -------------------
async def get_urls_content(
    body: TextModelRequest= Body(...))-> str : 
    """ text model requst is """

    logger.info("extract urls")
    urls= extract_urls(body.prompts)
    # -------------------async  scraping  ----------------------------- 
    try :  
        urls_contents= await fetch_all(urls) # async scrapping  ## result is .join (string) so no worries
        return urls_contents
    
    except as e: 
        logger.warning("error on fetching {e}")
        return " "


    


