#%%
import os
page_list = ["index.html","about_me.html","research.html","publications.html","vacancies.html","blog.html","contact.html"]
with open("html_template.html","r") as f:
    html_template = f.read()

import json
json_open = open('contents/meta_info.json', 'r')
meta_info = json.load(json_open)

nav_template = "\t\t<li><a href=PAGE_URL>TITLE</a></li>\n"
def make_nav(page):
    nav = ""
    for p in page_list:
        nav += nav_template.replace("PAGE_URL",p).replace("TITLE",p.replace(".html","").title())
    if lang == "":
        target = page.replace(".html","_jp.html")
        title = "Japanese"
    else:
        target = page.replace("_jp.html",".html")
        title = " English"
        nav = nav.replace(".html","_jp.html")
    nav += nav_template.replace("PAGE_URL",target).replace("TITLE",title)
    nav = nav.replace("Index","Home").replace("About_Me","About Me")
    return nav

def make_title(page):
    title = ""
    try:
        title =meta_info[page.replace(".html","")]["title"]
    except KeyError:
        pass
    if title =="":
        title = page.title()
    return title

def get_contents(page):
    content_file = page.replace(".html",f"{lang}_contents.html")
    try:
        with open(f"contents/{content_file}", "r") as f:
            contents = f.read()
    except FileNotFoundError: # no Japanese file
        contents = "No Japanese yet"
    return contents
for page in page_list:
    for lang in ["","_jp"]:
        save_file_name = page.replace(".html",f"{lang}.html")
        nav = make_nav(page)
        contents = get_contents(page)
        title = make_title(page)
        output_html = html_template.replace("NAV_BAR",nav).replace("CONTENTS",contents).replace("PAGE_TITLE",title)
        """
        with open(save_file_name, "w") as f:
            f.write(output_html)
        """