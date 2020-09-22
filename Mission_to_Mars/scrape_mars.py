from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import re
import time


def scrape_all():
    executable_path = {'\\c\\Users\\Franklin Troung\\Desktop\\Mission_to_Mars'}
    browser = Browser("chrome", *executable_path)
    news_title, news_paragraph = mars_news(browser)



def mars_news(browser):
    nasa_url="https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    try:
        article = soup.find("div", class_="list_text")
        news_p = article.find("div", class_="article_teaser_body").text
        news_title = article.find("div", class_="content_title").text
        news_date = article.find("div", class_="list_date").text
    except AttributeError:
        return None, None
    return news_title, news_p
    

def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    source = soup.find("img", class_="thumb")["src"]
    image = "https://jpl.nasa.gov"+ source
    image_url = image
    return image


def mars_facts():
    url="https://space-facts.com/mars/)"
    browser.visit(url)
    mars_table=pd.read_html(url)
    data_table=mars_table[0]
    mars_profile=data_table.rename(columns={0:'Description',1: "value"})
    return mars_profile.to_html(header=True, index=True)

def scrape_hemi(browser):
    hemispheres=['Cerberus Hemisphere Enhanced',
      'Schiaparelli Hemisphere Enhanced',
      'Syrtis Major Hemisphere Enhanced',
      'Valles Marineris Hemisphere Enhanced']
    hemisphere_url = []
 
    for info in hemispheres:
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.is_element_present_by_text(info, wait_time=1)
    info = browser.find_link_by_partial_text(info)
    info.click()
    image = browser.find_by_id('wide-image-toggle')
    image.click()
    soup = bs(browser.html, 'html.parser')
    photo = soup.body.find('img', class_='wide-image')
    photo_src = photo['src']
    photo_url = f"https://astrogeology.usgs.gov{photo_src}"
    hemisphere_url.append(photo_url)  
        return(photo_url)

    mars_hemisphere= [
    {"title": "Valles Marineris Hemisphere", "img_url": hemisphere_url[0]},
    {"title": "Cerberus Hemisphere", "img_url":hemisphere_url[1]},
    {"title": "Schiaparelli Hemisphere", "img_url": hemisphere_url[2]},
    {"title": "Syrtis Major Hemisphere", "img_url": photo_url[3]},]
    return mars_hemisphere

if __name__ == "__main__":
    print(scrape_all())