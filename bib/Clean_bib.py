
#%%
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:22:44 2020

@author: Hideshi_Ooka
"""
import pandas as pd
import re

def check(entry):
    if "=\"" in entry:
        print("This entry has quotation marks instead of parenthesses")
        print(entry)

def get_abbrv_key(journal):
    abbrv, j_key = "", ""
    for JOURNAL, ABBRV in abbrv_dict.items():
        if journal.upper() == JOURNAL:
            abbrv = ABBRV
            break
    if abbrv == "":
        abbrv = journal
        if abbrv not in abbrv_dict.values():
            print(f"Abbreviation not found for {journal}")
    for ABBRV,KEY in key_dict.items():
        if abbrv.upper() == ABBRV:
            j_key = KEY
    if j_key =="":
        j_key = abbrv.replace(" ", "").replace(".","")     
    return abbrv,j_key     

def restore_fullname(fullname):
    restored_fullname = fullname
    for JOURNAL, ABBRV in abbrv_dict.items():
        if fullname == ABBRV:
            restored_fullname = JOURNAL.title()
            break
    restored_fullname = restored_fullname.replace("Acs","ACS").replace("Rsc","RSC")
    return restored_fullname

def get_author_key(authors):
    if "other" in authors:
        print(f"check author list: {author}")
    author_key = authors.split(",")[0]
    if "-" in author_key:
        author_key = author_key.split("-")[0].capitalize() + author_key.split("-")[1].capitalize()
    if "mc" in author_key:
        author_key = author_key.split("mc")[0].capitalize() + author_key.split("-")[1].capitalize()
    author_key = re.sub(r"[^a-zA-Z0-9]", "", author_key)
    return author_key   

def format_title(title):
    return title.title().replace("Ph ","pH ")

def format_new_article(entry_dict):
    new_article = "@article{" + entry_dict["bib_key"] 
    for key in USE_KEYS[:-2]: 
        new_article += ",\n    " + key + " = {" + entry_dict[key] + "}"
    new_article += "}\n\n"
    return new_article

filename = "Publications.bib"
with open(filename, "r", encoding = "UTF-8") as f:
    bib_data = f.read() 
with open(filename.replace(".bib", "_bk.bib"), 'w') as f:
    f.write(bib_data)
bib_data =bib_data.replace("\n", "")
entries = bib_data.split("@")[1:]

### ABBREVIATE Journal Names
df = pd.read_csv('Journal_Abbreviations.csv', encoding = "UTF-8")
df = df.fillna("")
abbrv_dict = dict(zip(df.JOURNAL, df.ABBRV))
abbrv_dict = {JOURNAL.upper(): ABBRV for JOURNAL, ABBRV in abbrv_dict.items()}
key_dict = dict(zip(df.ABBRV, df.KEY))
key_dict = {ABBRV.upper(): KEY for ABBRV, KEY in key_dict.items()}

new_bib_data = ""
USE_KEYS = ["author", "journal","abbrv", "fullname","year", "volume","pages", "title", "j_key", "bib_key"]
ABBREVIATE = True

for entry in entries:
    entry = entry.rsplit("}}", 1)[0]
    if entry.split("{")[0] == "article": 
        entry_dict = {}
        for x in USE_KEYS:
            if x in entry:
                entry_dict[x] = entry.split(x,1)[1].split("{",1)[1].split("},")[0]
            else:
                entry_dict[x] = "XXX"
               
        entry_dict["abbrv"] = get_abbrv_key(entry_dict["journal"])[0]
        entry_dict["j_key"] = get_abbrv_key(entry_dict["abbrv"])[1]
        entry_dict["fullname"] = entry_dict["journal"]
        if ABBREVIATE == True:
            entry_dict["journal"] = entry_dict["abbrv"]
        if entry_dict["abbrv"] == entry_dict["fullname"]:
            entry_dict["fullname"] = restore_fullname(entry_dict["fullname"])
        # print(dict)
        author_key = get_author_key(entry_dict["author"])
        entry_dict["bib_key"] = author_key + entry_dict["year"] + entry_dict["j_key"]
        entry_dict["title"] = format_title(entry_dict["title"])
        new_entry = format_new_article(entry_dict)
    else:
        new_entry = "@" + entry + "}\n\n"
        # print(new_entry)
    new_bib_data += new_entry
  
                                   
with open(filename, 'w', encoding = "UTF-8") as f:
    f.write(new_bib_data)        



