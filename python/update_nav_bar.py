#%%
import os
import datetime
import json
def update_navbar(txt, lang):
    if lang == "":
        other_lang = "_JP"
        lang2_label = "Japanese"
    else:
        other_lang = ""
        lang2_label = "English"
    txt = txt.replace("LANG2_LABEL",lang2_label).replace("_LANG2", other_lang)
    txt = txt.replace("_LANG", lang)
    current_page = page.replace(".html","")
    txt = txt.replace("CURRENT_PAGE", current_page)
    return txt

def make_title(page):
    title = ""
    try:
        title =meta_info[page.replace(".html","")]["title"]
    except KeyError:
        pass
    if title =="":
        title = page.replace(".html","").title()
    print(title)
    return title

def get_contents(page):
    content_file = page.replace(".html",f"{lang}_contents.html")
    print(content_file)
    try:
        with open(f"../contents/{content_file}", "r",encoding="utf-8") as f:
            contents = f.read()
    except FileNotFoundError:
        with open(f"../contents/construction_contents.html", "r") as f:
            contents = f.read()
    return contents

html_list = [f for f in os.listdir("../") if f[-5:] == ".html"]
with open("../templates/html_template.html","r") as f:
    html_template = f.read()
nav_template = html_template.split("<!-- PAGE SPECIFICS -->")[0]
# update_navbar when necessary by updating template, then editing every html
#


#%%
"""
today = datetime.date.today().strftime('%Y/%m/%d')
page_list = ["index.html","about_me.html","research.html","publications.html","vacancies.html","blog.html","contact.html","presentations.html","funding.html","patents.html","awards.html"]
with open("../templates/html_template.html","r") as f:
    html_template = f.read()
json_open = open('../contents/meta_info.json', 'r')
meta_info = json.load(json_open)

for page in page_list:
    for lang in ["","_JP"]:
        output_html = html_template
        output_html = update_navbar(output_html, lang)
        save_file_name = page.replace(".html",f"{lang}.html")
        save_file_name = f"../{save_file_name}"
        contents = get_contents(page)
        title = make_title(page)
        output_html = output_html.replace("CONTENTS",contents).replace("PAGE_TITLE",title).replace("TODAY",today)
        with open(save_file_name, "w", encoding="utf-8") as f:
            f.write(output_html)
"""