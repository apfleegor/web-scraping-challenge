
# import dependencies
import requests
from bs4 import BeautifulSoup
import pymongo
import pandas as pd

# import splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 


# NASA Mars News

def mars_news():

    # go to the mars news site and extract the title and paragraph for the first news article

    # setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # mars news site url
    url = "https://www.redplanetscience.com"

    # use splinter to visit url
    browser.visit(url)

    # parse the page with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # get the first title
    header = soup.find("div", class_="content_title")
    news_title = header.text

    # get the first title's corresponding paragraph
    paragraph = soup.find("div", class_="article_teaser_body")
    news_p = paragraph.text

    # quit the browser
    browser.quit()
    
    return [news_title, news_p]


# JPL Mars Space Images—Featured Image

def mars_image_featured():

    # go to the jpl mars space images website and get the featured image url

    # setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # jpl mars space images url
    url = "https://spaceimages-mars.com/"

    # use splinter to visit url
    browser.visit(url)

    # parse the page with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # find the tag for the featured image
    image = soup.find("img", class_="headerimage fade-in")

    # get the relative link
    relative_link = image['src']

    # add the relative url to the main url
    featured_image_url = url + relative_link

    # quit the browser
    browser.quit()
    
    return featured_image_url


# Mars Facts

def mars_facts():

    # go to the mars facts website and get the table with facts

    # mars facts site url
    url = "https://galaxyfacts-mars.com/"

    # use pandas to scrape the site for tables
    table = pd.read_html(url)

    # create a dataframe with the table
    df = table[0]

    # fix the table for formatting
    df = df.rename(columns=df.iloc[0])
    df = df.rename(columns={"Mars - Earth Comparison": "Description"})
    df = df.set_index("Description")


    # convert the dataframe into a html table string
    html_table = df.to_html(classes="table table=striped")

    # remove the \n
    html_table = html_table.replace('\n', '')
    
    return html_table

# Mars Hemispheres

def extract_img (url):
    
    # setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # use splinter to visit url
    browser.visit(url)
    
    # parse the page with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    # find the first element in the container including the target image
    link = soup.find("div", class_="downloads").find("li")
    
    # get the relative link for the image
    link = link.a.get("href")
    
    # quit the browser
    browser.quit()
    
    # return the relative link
    return link

def mars_hemi():

    # visit the astrogeology website to get images for each mars hemisphere

    # setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # astrogeology site url
    url = "https://marshemispheres.com/"

    # use splinter to visit url
    browser.visit(url)

    # parse the page with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # find all the tags with the class itemLink product-item
    hemi_links = soup.find_all("a", class_="itemLink product-item")

    # quit the browser
    browser.quit()

    # create list for dictionaries with urls to go in
    hemisphere_image_urls = []

    # for each result
    for hemi in hemi_links:

        # if the h3 tag exists
        if (hemi.h3):

            # if the tag is not for the back button
            if (hemi.h3.text != "Back"):

                # get the title, removing the "enhanced" part
                title = hemi.h3.text
                title = title.replace(' Enhanced', '') 

                # if there is an href
                if (hemi.get("href")):

                    # get the relative link
                    href = hemi.get("href")

                    # create new url using url and the relative link
                    new_url = url + href

                    # call the extract_img method to get the relative url for the image
                    new_href = extract_img(new_url)

                    # create the full url for the image
                    img_url = url + new_href

                    # create dictionary for the hemisphere and corresponding image
                    image_dict = {"title": title,
                                 "img_url": img_url}

                    # add the dictionary to the list
                    hemisphere_image_urls.append(image_dict)
    
    return hemisphere_image_urls


# Create scrape_mars.py with above info

def scrape():
    
    news_title, news_p = mars_news()
    
    featured = mars_image_featured()
    
    facts_table = mars_facts()
    
    hemi_pics = mars_hemi()
    
    final_dict = {"title": news_title,
                 "news_p": news_p,
                 "featured_image": featured,
                 "table": facts_table,
                 "hemisphere_images": hemi_pics}
    
    return final_dict