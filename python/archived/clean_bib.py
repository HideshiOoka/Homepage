#%%
# -*- coding: utf-8 -*-
"""
@author: Hideshi_Ooka
"""
import pandas as pd
import re
from titlecase import titlecase
# https://github.com/ppannuto/python-titlecase
# pip install titlecase
journal_dict = "../achievements/Journal_Abbreviations.csv"

def check(entry):
    if "=\"" in entry:
        print("This entry has quotation marks instead of parenthesses")
        print(entry)
        # This warning shouldn't occur if bibtex is copied from G scholar

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
    j_key = re.sub(r"[^a-zA-Z0-9]", "", j_key)
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
        print(f"check author list: {authors}")
    author_key = authors.split(",")[0]
    if "-" in author_key:
        author_key = author_key.split("-")[0].capitalize() + author_key.split("-")[1].capitalize()
    if "mc" in author_key: ### check if this works properly
        author_key = author_key.split("mc")[0].capitalize()
    if " " in author_key:
        author_key = author_key.split(" ")[-1].capitalize()
    author_key = re.sub(r"[^a-zA-Z0-9]", "", author_key)
    return author_key   

def format_title(title):
    new_title = titlecase(title) # title.title()
    # print(new_title)
    return new_title

def format_new_article(entry_dict):
    new_article = "@article{" + entry_dict["bib_key"] 
    for key in USE_KEYS: 
        new_article += ",\n    " + key + " = {" + entry_dict[key] + "}"
    new_article += "}\n\n"
    new_article = new_article.replace("Ph ","pH ").replace("Ph-","pH-").replace("Ftir","FTIR").replace("Co2","CO2").replace("Co ","CO ").replace("Mos2","MoS2").replace("Cstr","CSTR").replace("Bep","BEP").replace("Feiv=O","FeIV=O").replace(r"Br{\O}Nsted",r"Br{\o}nsted").replace("Tca","TCA").replace("Brenda","BRENDA").replace("Kcat","kcat").replace("Volcano'S", "Volcano's").replace(r"Th\'Eorie G\'En\'Erale De L'Action",r"Th\'eorie G\'en\'erale De L'Action").replace("Sabio-Rk", "Sabio-RK").replace(r"Norskov",r"N{\o}rskov")
    return new_article

# A bit dirty, but the abbrv_dict is accessed in functions
df = pd.read_csv(journal_dict, encoding = "UTF-8")
df = df.fillna("")
df = df.sort_values(by="JOURNAL")
df.to_csv(journal_dict, index = False)

abbrv_dict = dict(zip(df.JOURNAL, df.ABBRV))
abbrv_dict = {JOURNAL.upper(): ABBRV for JOURNAL, ABBRV in abbrv_dict.items()}
key_dict = dict(zip(df.ABBRV, df.KEY))
key_dict = {ABBRV.upper(): KEY for ABBRV, KEY in key_dict.items()}
USE_KEYS = ["author", "journal","abbrv", "fullname","year", "volume","pages", "title", "j_key", "bib_key","preprint","url","status","notes","type"]
ABBREVIATE = True

# filename = "../achievements/Publications.bib"
# filename = "UBP1b.bib"
# filename = "../achievements/Dissipative_CRN.bib"
def save_cleaned_bib(filename = "../achievements/Publications.bib"):
    with open(filename, "r", encoding = "UTF-8") as f:
        bib_data = f.read() 
    with open(filename.replace(".bib", "_bk.bib"), 'w') as f:
        f.write(bib_data)
    bib_data =bib_data.replace("\n", "")
    entries = bib_data.split("@")[1:]
    new_bib_data = ""
    for entry in entries:
        entry = entry.rsplit("}}", 1)[0]
        # print(entry)
        if entry.split("{")[0] == "article": 
            entry_dict = {}
            for x in USE_KEYS:
                if x in entry:
                    # print(x,entry)
                    entry_dict[x] = entry.split(x,1)[1].split("{",1)[1].split("},")[0]
                else:
                    entry_dict[x] = ""
            entry_dict["abbrv"] = get_abbrv_key(entry_dict["journal"])[0]
            entry_dict["j_key"] = get_abbrv_key(entry_dict["abbrv"])[1]
            entry_dict["fullname"] = entry_dict["journal"]
            if ABBREVIATE == True:
                entry_dict["journal"] = entry_dict["abbrv"]
            if entry_dict["abbrv"] == entry_dict["fullname"]:
                entry_dict["fullname"] = restore_fullname(entry_dict["fullname"])
            author_key = get_author_key(entry_dict["author"])
            entry_dict["bib_key"] = author_key + entry_dict["year"] + entry_dict["j_key"]
            entry_dict["title"] = format_title(entry_dict["title"])
            new_entry = format_new_article(entry_dict)
        else:
            new_entry = "@" + entry.replace(",  ",",\n  ")
            title = new_entry.split(r"title={")[1].split(r"},")[0].strip()
            print(title)
            formatted_title = format_title(title)
            new_entry = new_entry.replace(title, formatted_title)+"}}\n\n"
        new_bib_data += new_entry
    with open(filename, 'w', encoding = "UTF-8") as f:
        f.write(new_bib_data)        



#%%
"""
Aarnling B\r{a}\r{a}th
N\o{}rskov
\`{o}	ò	grave accent
\'{o}	ó
\"{o}	ö
\c{c}	ç
\r{a}	å
Henri1902CRHebdS\'eancesAcadSci
Th\'Eorie G\'En\'Erale De L'Action
"""


# code needs to be updated
# Search Br{\O}nsted--Evans--Polanyi in the title as n will be converted to N


