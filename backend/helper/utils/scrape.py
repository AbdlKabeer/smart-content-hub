import asyncio
import ssl
import aiohttp
from newspaper import Article
import certifi

from account.models import Article as ArticleModel
from django.db import models
from asgiref.sync import sync_to_async



from bs4 import BeautifulSoup
import aiohttp
import ssl
import certifi
import logging
import traceback


class ArticleManager:
    def __init__(self, param:str = None):
        self.param = param

    def ssl_cont(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        return conn

    async def fetch(self, session, url):
        headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683 Safari/537.36 OPR/57.0.3098.91'
        }
        async with session.get(url, headers=headers) as response:
            return await response.text()
        
    async def fetch_post(self, session, url, body):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '_ga=GA1.1.1789951575.1705762279; ASP.NET_SessionId=sjc5onalon0mnfq32g425y1e; _ga_HH2TRTCF3Y=GS1.1.1711094683.11.1.1711094804.0.0.0',
            'Origin': 'https://www.edmontonpolice.ca',
            'Referer': 'https://www.edmontonpolice.ca/CrimeFiles/EdmontonsMostWanted',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }

        async with session.post(url, headers=headers, data=body) as response:
            return await response.text()

    def parse(self, html):
        soup = BeautifulSoup(html,'html.parser')
        return soup

    
    async def search(self, **kwargs):
        async with aiohttp.ClientSession(connector=self.ssl_cont()) as session:
            results = []
            try:
                
                try:
                    # if not page_exit: break
                    url = f'https://www.teachermagazine.com/sea_en/category/short-articles/p2'  
                    
                    html = await self.fetch(session, url, **kwargs)
                                
                    body = self.parse(html)

                    section = body.find('section', attrs={'id': 'page-content'})

                    article_cards = section.find_all('div', attrs={'class': 'article-listing-card'})

                    print("******"*20)
                    for article in article_cards:
                        link = article.find('a')['href']
                        results.append(link)

                except:pass



                return results
            except Exception as e:
                logging.error(str(e))
                return results
            




# data = asyncio.run(ArticleManager().search())
# print(data)

# import asyncio, json
# res = asyncio.run(EUSanctionsTracker("Wadim Konstantinowitsch KALININ").search())
class GoogleDataHandler:

    @staticmethod
    def ssl_cont():
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        return conn

    @staticmethod
    async def scrape_article(url):
        article_data = {}

        try:
            # Initialize the Article object
            article = Article(url)
            article.download()
            article.parse()

            # Collect article properties
            article_data['title'] = article.title
            article_data['authors'] = ', '.join(article.authors) if article.authors else ""
            article_data['publish_date'] = article.publish_date
            article_data['source_url'] = article.source_url
            article_data['text'] = article.text
            article_data['keywords'] = ', '.join(article.keywords) if article.keywords else ""
            article_data['top_image'] = article.top_image
            article_data['meta_description'] = article.meta_description
            article_data['summary'] = article.summary

            print(article.text)
            print("****"*20)
            print(article.title)
            # Save the scraped data to the database using sync_to_async
            article_obj = await sync_to_async(ArticleModel.objects.create)(
                title=article_data['title'],
                authors=article_data['authors'],
                publish_date=article_data['publish_date'],
                source_url=article_data['source_url'],
                text=article_data['text'],
                keywords=article_data['keywords'],
                top_image=article_data['top_image'],
                meta_description=article_data['meta_description'],
                summary=article_data['summary']
            )

            return True
            # return article_obj

        except Exception as e:
            # Handle any exceptions that might occur
            print(f"Error scraping article: {e}")
            return None


# links = asyncio.run(ArticleManager().search())
# print(links)
# # Running the asynchronous function
# for link in links:
#     data = asyncio.run(GoogleDataHandler.scrape_article(link)) 

    
