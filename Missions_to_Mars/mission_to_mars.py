from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_ = 'content_title')
    news_title = news_title[1].find('a').get_text()

    print(news_title)

    news_p = soup.find_all('div', class_ = 'article_teaser_body')
    news_p = news_p[0].get_text()

    print(news_p)

    browser.quit()

    #--------------------------------------------------------------------------------#
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image = soup.find('a', class_ = 'button fancybox')['data-fancybox-href']

    nasa_url = 'https://www.jpl.nasa.gov'

    featured_image_url = nasa_url + featured_image
    print(featured_image_url)

    browser.quit()
    #--------------------------------------------------------------------------------#
    url = 'https://space-facts.com/mars/'

    table = pd.read_html(url)
    table

    mars_table = table[0]

    mars_table = mars_table.rename(columns = {0: 'Mars Facts', 1:''})
    mars_table = mars_table.set_index('Mars Facts')

    mars_html_table = mars_table.to_html('../Output/mars_table.html')

    #--------------------------------------------------------------------------------#
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    for i in range(4):
        title = soup.find_all('h3')[i].get_text()
        browser.find_by_tag('h3')[i].click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        image_url = soup.find('a', text = 'Sample')['href']
        
        hemisphere_image_urls.append({
            'title': title,
            'image_url': image_url
        })

        browser.back()

    browser.quit()

    scraped_data = {
        "news_title" : news_title, 
        "news_p" : news_p, 
        "featured_image" : featured_image,
        "mars_table" : mars_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    return scraped_data