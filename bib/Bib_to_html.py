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


filename = "Publications.bib"
with open(filename, encoding = "UTF-8") as f:
    bib_data = f.read().replace("\n", "")
entries = bib_data.split("@")[1:]

out_html = ""
year_header = "2030"
for entry in entries:
    authors = entry.split("author = {")[1].split("},")[0]
    authors = sort(authors)
    journal = entry.split("journal = {")[1].split("},   ")[0]
    year = entry.split("year = {")[1].split("},   ")[0]
    volume = entry.split("volume = {")[1].split("},   ")[0]
    pages = entry.split("pages = {")[1].split("},   ")[0].replace("--","-")
    title = entry.split("title = {")[1].split("}}")[0]
    if year < year_header:
        year_header = year
        out_html += "\t<h2>{}</h2>\n".format(year_header)
    out_html += "\t\t<li>{} \"{}\", <i>{}</i>, <b>{}</b>, <i>{}</i>, {}.<br>\n\n".format(authors, title, journal, year, volume, pages)

out_html = out_html.replace("MoS2", "MoS<sub>2</sub>").replace("CO2", "CO<sub>2</sub>").replace("{\`e}","&egrave")

with open(filename.replace("bib","html"), 'w') as f:
    f.write(out_html)        









