# -*- coding: utf-8 -*-
#%%
"""
Created on Thu Dec 10 17:22:44 2020

@author: Hideshi_Ooka
"""
import pandas as pd
import re

def sort(authors):
    sorted_authors = ""
    for a in authors.split(" and "):
        last,first  = a.split(", ")
        sorted_authors += first + " " + last + ", "
    sorted_authors = sorted_authors[:-2]        
    return sorted_authors

with open("Publications.bib", encoding = "UTF-8") as f:
    bib_data = f.read().replace("\n", "")
entries = bib_data.split("@")[1:]

corresponding_authors = str(bib_data.count("Ooka*"))
first_authors = str(bib_data.count("@article{Ooka"))
out_html = ""
year_header = "2030"
for entry in entries:
    entry = entry.split("}}")[0]
    authors = entry.split("author = {")[1].split("},")[0]
    authors = sort(authors)
    journal = entry.split("journal = {")[1].split("},   ")[0]
    year = entry.split("year = {")[1].split("},   ")[0]
    title = entry.split("title = {")[1].split("},")[0]
    volume = entry.split("volume = {")[1].split("},   ")[0]
    pages = entry.split("pages = {")[1].split("},   ")[0].replace("--","-")
    if "rxiv" in journal.lower():
        doi = entry.split("doi = {")[1].split("},   ")[0]
        status = entry.split("status = {")[1].split("},   ")[0]
        volume = status # replace the volume and pages entry with doi and review status
        pages = doi

    if year < year_header:
        year_header = year
        out_html += "\t<h2>{}</h2>\n".format(year_header)
    out_html += f"\t\t<li>{authors} \"{title}\", <i>{journal}</i>, <b>{year}</b>, <i>{volume}</i>, {pages}.<br>\n\n"

out_html = out_html.replace("MoS$_2$", "MoS<sub>2</sub>").replace("CO$_2$", "CO<sub>2</sub>").replace("{\`e}","&egrave").replace("MnO$_2$", "MnO<sub>2</sub>")

with open("publications_template.html","r") as f:
    template = f.read()

out_html = template.replace("<!-- ADD_PUBLICATION_LIST_HERE-->", out_html).replace("CORRESPONDING_AUTHORS",corresponding_authors).replace("FIRST_AUTHORS", first_authors)
    
translate_dict = {"Scientific Publications":"論文",
                  "Corresponding Author":"責任著者",
                  "First Author":"筆頭著者",
                  "Last Author":"最終著者",
                  "Patents":"知財・特許"}    

def translate(txt):
    for k,v in translate_dict.items():
        print(k,v)
        txt = txt.replace(k,v)
    return txt   
out_html_jp = translate(out_html)


with open("../contents/publications_contents.html", 'w') as f:
    f.write(out_html)    
with open("../contents/publications_jp_contents.html", 'w') as f:
    f.write(out_html_jp)        








