#%%
import pandas as pd
import numpy as np
import bibtexparser
from docx import Document
from docx.shared import RGBColor
# date 20171101 for the CSRS Interim report might be off
# from docx.shared import Pt
# search Km and $ and { for TeX

def bib2df(bib_file, sort = True):
    with open(bib_file) as f:
        bib = bibtexparser.load(f)
    df = pd.DataFrame(bib.entries)    
    cols = ["ID", "author","journal","year","volume","pages", "doi", "notes", "ENTRYTYPE"]
    missing_cols = [item for item in df.columns if item not in cols]
    cols += missing_cols
    df = df[cols].sort_values(by=["year"], ascending = False)   
    df = df.fillna("")
    num_publications =df.shape[0]
    corresponding_authors = df.author.str.contains("Ooka\*").sum()
    first_authors = df.ID.str.contains("Ooka").sum()
    print(num_publications, corresponding_authors, first_authors)
    return df

def write_entry(i, entry): # need to write the df 
    ID, authors, journal, year, volume, pages, doi, notes, ENTRYTYPE, type, title, fullname, abbrv, status = entry
    authors = sort(authors)
    print(notes,doi,status)
    p = doc.add_paragraph(f"{i+1}.  ")
    ### Authors:
    p = add_formatted_authors(p,authors)
    p.add_run(":") #################
    p.add_run(" \"").bold = True
    p = add_formatted_title(p,title) 
    p.add_run("\" ").bold = True
    p.add_run(journal).italic = True
    p.add_run(", ")
    p.add_run(volume)
    p.add_run(", (")
    p.add_run(year)
    p.add_run("), ")
    if pages != "":
        p.add_run(pages)
    else: # it doesn't have pages
        p.add_run(doi) # it must have doi
        p.add_run(" (")
        p.add_run(status).italic = True
        p.add_run(")")
    p.add_run(".").add_break()
    if notes != "":
        if LANG == "_JP":
            notes = notes.replace("Representative Paper", "代表論文")
        comment = p.add_run(notes)
        comment.font.bold = True
        comment.font.name = "Arial"
        # comment.font.underline = True
        comment.font.color.rgb = RGBColor.from_string("B10026")
        comment.add_break()

def sort(authors):
    sorted_authors = ""
    for a in authors.split(" and "):
        last,first  = a.split(", ")
        sorted_authors += first + " " + last + ", "
    sorted_authors = sorted_authors[:-2]        
    return sorted_authors
def add_formatted_title(p,title):  
    title = title.replace("--","-")   # -- in SPET
    if "CO" not in p.text and "MoS2" not in p.text:
        p.add_run(title).bold = True
        return p
    else:
        # break the runs? or do something?# # CO2, MoS2        
        p.add_run(title).bold = True # need some kind of formatting
        return p

def add_formatted_authors(p,authors):
    my_name = "Hideshi Ooka"
    try:
        before, after = authors.split(my_name)
    except ValueError:
        if LANG == "_JP":
            my_name = "大岡英史"
            before, after = authors.split(my_name)
    p.add_run(before)
    me = p.add_run(my_name)
    me.font.underline = True
    me.font.bold = True
    p.add_run(after)
    return p

def make_publication_list(bib_file, separate_reviews = False):
    header = "Academic Publications (All Peer Reviewed)"
    if LANG == "_JP":
        header = "学術論文 (査読あり)"
    doc.add_heading(header, level=1)
    
    df = bib2df(bib_file)
    N = df.shape[0]
    num_original = 0
    if separate_reviews == True:
        df = df.sort_values(by = ["type","year"], ascending = [True, False])
        num_original = df[df["type"]=="original"].shape[0]
        doc.add_paragraph(f"{num_original}")
    for i in range(N):
        entry = df.iloc[i]
        write_entry(i, entry)
        


def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date

months = ["","January","February","March","April","May","June","July","August","September","October","November","December"]
def make_funding_list(funding_csv):
    header = "Funding (Japanese Titles were Translated to English)"
    PI_text = "Principal Investigator"
    Co_PI_text = "Co-Investigator"
    unit = "yen"
    if LANG == "_JP":
        header = "外部資金獲得実績"
        PI_text = "研究代表者"
        Co_PI_text = "研究分担者"
        unit = "円"
    doc.add_heading(header, level=1)
    df = pd.read_csv(funding_csv)
    N = df.shape[0]
    for i in range(N):
        data = df.iloc[i]
        start,finish,title, name, source, PI, amount, unit = data[["Start","Finish","Title","PJ_Name","Funding_Source","PI","Amount","Unit"]]
        if PI == "PI":
            PI = PI_text
        else:
            PI = Co_PI_text
        p = doc.add_paragraph(f"{i+1}.  ")
        p.add_run(f"{source} {name} ({PI})\n")
        p.add_run(" \"").bold = True
        p = add_formatted_title(p,title) 
        p.add_run("\" ").bold = True
        start = str(start)
        finish = str(finish)
        formatted_start = start[:4] + " " + months[int(start[4:])]
        formatted_finish = finish[:4] + " " +months[int(finish[4:])]
        p.add_run(f"({formatted_start} - {formatted_finish}, {amount} {unit})").add_break()

def make_award_list(award_csv):
    header = "Awards (Japanese Titles were Translated to English)"
    if LANG == "_JP":
        header = "受賞歴"
    doc.add_heading(header, level=1)
    df = pd.read_csv(award_csv)
    N = df.shape[0]
    for i in range(N):
        data = df.iloc[i].astype(str)
        date,prize,origin,notes = data[["Date","Prize","From","Notes"]]
        date = str(date)
        date = f"{date[:4]}/{date[4:6]}/{date[6:]}"
        p = doc.add_paragraph(f"{i+1}.  ")
        p.add_run(f"{prize}").bold = True
        p.add_run(f", {origin} ({date}).").add_break()
        if notes !="nan":
            print(notes)
            comment = p.add_run(notes)
            comment.font.bold = True
            # comment.font.underline = True
            comment.font.color.rgb = RGBColor.from_string("B10026")
            comment.add_break()

def make_patent_list(patent_csv):
    header = "Patents"
    if LANG == "_JP":
        header = "知財・特許"
    doc.add_heading(header, level=1)
    df = pd.read_csv(patent_csv)
    N = df.shape[0]
    for i in range(N):
        data = df.iloc[i,:5]
        date,status,authors,title,ID = data
        authors = authors.replace(" and",",")
        p = doc.add_paragraph(f"{i+1}.  ")
        ### Authors:
        p = add_formatted_authors(p,authors)
        p.add_run(" \"")
        p = add_formatted_title(p,title) 
        p.add_run("\", ")
        p.add_run(f"{ID} ({status}).").add_break()



def make_press_list(press_csv):
    pass ##########
def make_presentation_list(presentation_csv):
    header = "Presentations (Japanese Titles were Translated to English)"
    if LANG == "_JP":
        header = "学会発表"
    doc.add_heading(header, level=1)
    format_list = ["Invited","Oral","Poster"]
    format_list_JP = ["【招待講演】","【口頭発表】","【ポスター発表】"]
    all_df = pd.read_csv(presentation_csv)
    for j,df in enumerate(format_list):
        df = all_df[all_df["Format"] == format_list[j]]
        df = df.sort_values(by = "Date", ascending = False)
        N = df.shape[0]
        sub_header = format_list[j] + " Presentations"+f" ({N})"
        if LANG == "_JP":
            sub_header = format_list_JP[j]
        doc.add_heading(sub_header, level=2)
        for i in range(N):
            data = df.iloc[i].astype(str)
            date,conference,venue,country_or_city,title,authors,format,notes = data[:8]
            formatted_date = format_date(date)
            p = doc.add_paragraph(f"{i+1}.  ")
            p = add_formatted_authors(p,authors)
            p.add_run(f' "{title}"').bold = True
            p.add_run(f" {conference}, {venue}, {country_or_city} ({formatted_date}).").add_break()
            if notes !="nan":
                comment = p.add_run(notes)
                print(notes)
                comment.font.bold = True
                # comment.font.underline = True
                comment.font.color.rgb = RGBColor.from_string("B10026")
                comment.add_break()



doc = Document("Publication_List_Template.docx")
# items = ["Heading", "Publications", "Presentations","Patents","Press","Funding","Awards"]
# for item in items:
#     doc.add_paragraph(item,style = "Heading 1")


LANG = "" # English    
LANG = "_JP" # Japanese



make_publication_list(f"Publications.bib", separate_reviews=True)
make_presentation_list(f"Presentations{LANG}.csv")
make_funding_list(f"Funding{LANG}.csv")
make_patent_list(f"Patents{LANG}.csv")
make_award_list(f"Awards{LANG}.csv")
# make_others_list("Others.csv")
# make_press_list("Press.csv")
doc.save(f"Publication_list{LANG}.docx")


"""
standard write_entry
def write_entry(i, entry): # need to write the df 
    ID, authors, journal, year, volume, pages, doi, notes, ENTRYTYPE, type, title, fullname, abbrv, status = entry
    authors = sort(authors)
    print(notes,doi,status)
    p = doc.add_paragraph(f"{i+1}.  ")
    ### Authors:
    p = add_formatted_authors(p,authors)
    p.add_run(" \"").bold = True
    p = add_formatted_title(p,title) 
    p.add_run("\" ").bold = True
    p.add_run(journal).italic = True
    p.add_run(", ")
    p.add_run(year).bold = True
    p.add_run(", ")
    if volume != "":
        p.add_run(volume).italic = True
        p.add_run(", ")
    if pages != "":
        p.add_run(pages)
    else: # it doesn't have pages
        p.add_run(doi) # it must have doi
        p.add_run(" (")
        p.add_run(status).italic = True
        p.add_run(")")
    p.add_run(".").add_break()
    if notes != "":
        if LANG == "_JP":
            notes = notes.replace("Representative Paper", "代表論文")
        comment = p.add_run(notes)
        comment.font.bold = True
        comment.font.name = "Arial"
        # comment.font.underline = True
        comment.font.color.rgb = RGBColor.from_string("B10026")
        comment.add_break()
"""