from playwright.sync_api import sync_playwright
import re
import openai
import pandas as pd

def clean_whitespace(s):
    return re.sub('\n+', ' ', s.strip())
    
def remove_js(html_content):
    # Regular expression pattern to find script tags and their contents
    pattern = r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>'

    # Using re.sub() to replace the found script tags with an empty string
    cleaned_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE)

    return cleaned_content
    
def get_all_links(url):
    # Start Playwright in synchronous mode
    print(url)
    
    with sync_playwright() as p:
        all_text = []
        # Launch the browser
        browser = p.chromium.launch()
        
        # Open a new page
        page = browser.new_page()
        
        # Navigate to the target URL
        try:
            page.goto(url)
            links = page.query_selector_all("//a[@href]")
        except:
            return("no_site_content")
        
        # Extract all links on the page
        
        urls = [link.get_attribute('href') for link in links if url.replace("https", "").replace("http", "").replace(".com/", "") in link.get_attribute('href')]
        
        #all_text = []
        
        for url2 in urls:
            try:
                page.goto(url2)
                #text_elements = page.query_selector_all("p, div, span, h1, h2, h3, h4, h5, h6, li, a")
                #texts = " ".join([element.text_content() for element in text_elements if element.text_content() is not None])
                #texts = remove_js(clean_whitespace(texts))
                #all_text.append(texts)
                #print(page.text_content("body")) #print(page.inner_html("*")) #.text_content()
            
                text = page.text_content("body")
                text = remove_js(clean_whitespace(text))
                all_text.append(text)
            except:
                pass

        browser.close()
        
        return(" ".join(all_text))


df = pd.read_csv("~/5_missing_coffee_stores_working_website.csv")
print(len(df))

missing_stores_working_site_text = [get_all_links(x["URL"]) for x in df.to_dict(orient = 'records')]

#print(missing_stores_working_site_text)
df["Site Content"] = missing_stores_working_site_text
df.to_csv("~/6_missing_coffee_stores_working_website_with_site_content.csv", index = False)
