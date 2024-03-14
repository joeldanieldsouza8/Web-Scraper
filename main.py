from bs4 import BeautifulSoup 
import requests 
import re

search_term = input("What product do you want to search for? ")

url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"

page_content = requests.get(url).text # Get the HTML of the page 
doc = BeautifulSoup(page_content, "html.parser") # Parse the HTML of the page

page_text = doc.find(class_="list-tool-pagination-text").strong
# print(page_text)

pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1]) # Get the number of pages
# print(pages)

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
    page_content = requests.get(url).text # Rename variable here
    doc = BeautifulSoup(page_content, "html.parser")
    div = doc.find(class_ = "item-cells-wrap border-cells short-video-box items-grid-view four-cells expulsion-one-cell")
    
    items = div.find_all(text=re.compile(search_term)) # Find all items explicitly with the search term in the name 
    for item in items:
        parent = item.parent # Get the parent of the current item
        # link = None # Initialize the link variable
        
        # If the parent is an anchor tag, get the link
        if parent.name != "a":
            continue
        else:
            link = parent["href"] # Get the link from the anchor tag 
            next_parent = item.find_parent(class_ = "item-container") # Get the closest first match parent of the current item
            
            try:
                price = next_parent.find(class_="price-current").strong.string # Get the price of the current item
                # print(price)
                items_found[item] = {"price": int(price.replace(",", "")), "link": link} # On each iteration, add the current item to the dictionary with the price and link
            except:
                pass

# print(items_found)

# eg) items_found = {"item1": {"price": 100, "link": "www.example.com/item1"}, "item2": {"price": 200, "link": "www.example.com/item2"}}
sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"]) # Sort the items by price

for item in sorted_items:
    print(item[0])
    print(f"{item[1]['price']} CAD")
    print(item[1]["link"])
    print("---------------------------")
