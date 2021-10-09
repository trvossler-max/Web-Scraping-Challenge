# import necessary libraries
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():

    # URL for scraping Mars news
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title
    news_title = soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_article = soup.find_all('div', class_='article_teaser_body')[0].text
    
    #url for scraping space images
    url_jpl = 'https://spaceimages-mars.com/'
    browser.visit(url_jpl)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Create variable to find the image and the variable for the url
    image_path = soup.find_all('img', class_='headerimage fade-in')[0]['src']
    featured_image_url = url_jpl + image_path
    
    #url for scraping Mars facts
    url_mars = 'https://galaxyfacts-mars.com/'
    #Use Pandas to read the HTML table
    tables = pd.read_html(url_mars)
    # Convert list to a pandas dataframe for table 2
    mars2_df = tables[1]
    mars2_df.columns = ['Mars Planet Profile', 'Value']
    #Drop first rown and set index
    mars2_df = mars2_df.iloc[1:]
    mars2_df.set_index('Mars Planet Profile', inplace=True)
    #Convert table to an HTML table string
    mars_html_table = mars2_df.to_html()
    #Strip unwanted lines
    mars_html_table = mars_html_table.replace('\n', '')

    # url for scraping mars hemisphere title and image
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract elements
    mars_hemi = soup.find('div', class_='collapsible results')
    mars_items = mars_hemi.find_all('div', class_='item')

    hemi_image_urls = []

    #iterate through hemispheres
    for i in mars_items:
        #collect title
        hemisphere = i.find('div', class_='description')
        title = hemisphere.h3.text
        #collect image
        hemi_url = hemisphere.a['href']
        browser.visit(url + hemi_url)
        img_html = browser.html
        img_soup = BeautifulSoup(img_html, 'html.parser')
        img_link = img_soup.find('div', class_='downloads')
        img_url = img_link.find('li').a['href']
        img_full_url = url + img_url
        # Create Dictionaries
        img_dict = {}
        img_dict['Title'] = title
        img_dict['img_url'] = img_full_url
        hemi_image_urls.append(img_dict)
    
    # Create dictionary
    mars_dict = {
        'news_title': news_title,
        'news_paragraph': news_article,
        'featured_image': featured_image_url,
        'mars_table': str(mars_html_table),
        'hemisphere_image': hemi_image_urls}
    
    # Close the browser after scraping
    browser.quit()
 
    # Return results
    return mars_dict
