import logging
import asyncio 
import re 
import aiohttp
from bs4 import BeautifulSoup 
from loguru import logger 


def extract_url(text: str) -> list[str]:
    url_pattern = r"(?P<url>https?:\/\/[^\s]+)"
    urls= re.findall(url_pattern , text)
    print("here")
    return urls 


def parse_inner_text(html_string: str)-> str:
    soup = BeautifulSoup(html_string, features='lxml')
    content= soup.find("div", id= "mw-content-text")
    if content:
        return content.get_text() 

    logger.warning("coud't parse the HTMl content")
    return ""


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    try : 
        async with session.get(url) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch {url}: Status {response.status}")
                return " "

            html_string= await response.text()
            return parse_inner_text(html_string)

    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return ""

async def fetch_all(urls: list[str])-> str:
    headers = {
        "User-Agent": "MyWikiScraper/1.1 (https://example.com/bot; bot-owner@gmail.com)",
        "Accept-Encoding": "gzip"  # Improves performance as per Wikimedia tips
    }


    async with aiohttp.ClientSession(headers = headers) as session:

                logging.info("fetching started")
                results= await asyncio.gather(
                    *[fetch(session, url) for url in urls], return_exceptions= True

                )

    sucess_results= [result for result in results if isinstance(result, str)]
    if len(results) != len(sucess_results):
        logger.warning("some urls could't not be fetched ")

    return " ".join(sucess_results)



if __name__ == "__main__":
    wikipedia_urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Asynchronous_I/O",
        "https://en.wikipedia.org/wiki/Web_scraping",
    ]

    text = asyncio.run(fetch_all(wikipedia_urls))
    print(text[:1000])  # print first 1000 chars



