#%%
import pandas as pd
import numpy as np
from docx import Document
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_LINE_SPACING
import re
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from CV_utils import sort_authors #,quote

# date 20171101 for the CSRS Interim report might be off
#%%
def h1(text):
    yellow_background = parse_xml(r'<w:shd {} w:fill="#FFF2CC"/>'.format(nsdecls('w')))
    tbl = doc.add_table(1,1)
    tbl.cell(0,0).text = text
    tbl.rows[0].cells[0]._tc.get_or_add_tcPr().append(yellow_background)
    header = tbl.cell(0,0).paragraphs[0].runs[0].font.name = "Arial" # if japanese, 游ゴシック
    header = tbl.cell(0,0).paragraphs[0].runs[0].font.bold = True
    header = tbl.cell(0,0).paragraphs[0].runs[0].font.size = Pt(14)
    # tbl.rows.height = Pt(64)
    # tbl.line_spacing = WD_LINE_SPACING.MULTIPLE(5) # Pt(18) # WD_LINE_SPACING.EXACTLY

def h2(text):
    p = doc.add_paragraph()
    header = p.add_run(text)
    header.font.name = "Arial"
    header.font.size = Pt(14)
    header.font.underline = True
    header.font.bold = True
    
def add_formatted_title(p,title):
    quotes = ['"','"']
    if title.isascii() == False:
        quotes = ['「','」']
    p.add_run(f" {quotes[0]}").bold = True
    title = title.replace("--","-")   # -- in SPET
    if "$_" not in title: # no subscripts
        p.add_run(title).bold = True
    else: 
        substrings = title.split(r"$_")
        for substring in substrings:
            if "$" in substring:
                subscript, upright = substring.split("$")
            else:
                subscript, upright = "", substring
            sub_text = p.add_run(subscript)
            sub_text.font.subscript = True
            sub_text.font.bold = True
            p.add_run(upright).bold = True
    p.add_run(quotes[1]).bold = True
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

def write_entry(i, entry): # need to write the df 
    ID, authors, journal, year, volume, pages, doi, notes, ENTRYTYPE, type, title, fullname, abbrv, status = entry
    authors = sort_authors(authors)
    p = doc.add_paragraph(f"{i+1}.\t")
    p = add_formatted_authors(p,authors) ### Authors:
    p = add_formatted_title(p,title) 
    p.add_run(journal).italic = True
    p.add_run(", ")
    p.add_run(year).bold = True
    p.add_run(", ")
    if pages != "":
        p.add_run(volume).italic = True
        p.add_run(", ")
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

def make_publication_list(csv_file, separate_reviews = False):
    # wrote 0 in the volume of Publications.csv to make the volume read as int
    df = pd.read_csv(csv_file, index_col = 0).fillna("").astype(str)
    N = df.shape[0]
    num_original = 0
    header = "Academic Publications (All Peer Reviewed)"
    sub_headers = ["Original Papers","Reviews"]
    unit = ""
    if LANG == "_JP":
        header = "学術論文 (査読あり)"
        sub_headers = ["原著論文","総説"]
        unit = " 報"
    h1(header) # doc.add_heading(header, level=1)
    if separate_reviews == True:
        df = df.sort_values(by = ["type","year"], ascending = [True, False])
        num_original = df[df["type"]=="original"].shape[0]
        num_reviews = N - num_original
        for i in range(N):
            if i == 0:
                h2(f"{sub_headers[0]}: {num_original}{unit}")
            if i == num_original:
                h2(f"{sub_headers[1]}: {num_reviews}{unit}")
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
    h1(header) # doc.add_heading(header, level=1)
    df = pd.read_csv(funding_csv)
    N = df.shape[0]
    for i in range(N):
        data = df.iloc[i]
        start,finish,title, name, source, PI, amount, unit_ = data[["Start","Finish","Title","PJ_Name","Funding_Source","PI","Amount","Unit"]] # change variable name later
        if PI == "PI":
            PI = PI_text
        else:
            PI = Co_PI_text
        p = doc.add_paragraph(f"{i+1}.  ")
        p.add_run(f"{source} {name} ({PI})\n")
        p = add_formatted_title(p,title) 
        start = str(start)
        finish = str(finish)
        formatted_start = start[:4] + " " + months[int(start[4:])]
        formatted_finish = finish[:4] + " " +months[int(finish[4:])]
        p.add_run(f"({formatted_start} - {formatted_finish}, {amount} {unit})").add_break()

def make_award_list(award_csv):
    header = "Awards (Japanese Titles were Translated to English)"
    if LANG == "_JP":
        header = "受賞歴"
    h1(header) # doc.add_heading(header, level=1)
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
            comment = p.add_run(notes)
            comment.font.bold = True
            # comment.font.underline = True
            comment.font.color.rgb = RGBColor.from_string("B10026")
            comment.add_break()

def make_patent_list(patent_csv):
    header = "Patents"
    if LANG == "_JP":
        header = "知財・特許"
    h1(header) # doc.add_heading(header, level=1)
    df = pd.read_csv(patent_csv)
    N = df.shape[0]
    for i in range(N):
        data = df.iloc[i,:5]
        date,status,authors,title,ID = data
        authors = authors.replace(" and",",")
        p = doc.add_paragraph(f"{i+1}.  ")
        ### Authors:
        p = add_formatted_authors(p,authors)
        p = add_formatted_title(p,title) 
        p.add_run(f" {ID} ({status}).").add_break()



def make_presentation_list(presentation_csv):
    header = "Presentations (Japanese Titles were Translated to English)"
    if LANG == "_JP":
        header = "学会発表"
    h1(header) # doc.add_heading(header, level=1)
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
        h2(sub_header) # doc.add_heading(sub_header, level=2)
        
        for i in range(N):
            data = df.iloc[i].astype(str)
            date,conference,venue,country_or_city,title,authors,format,notes = data[:8]
            formatted_date = format_date(date)
            p = doc.add_paragraph(f"{i+1}.  ")
            p = add_formatted_authors(p,authors)
            p = add_formatted_title(p,title) 
            p.add_run(f" {conference}, {venue}, {country_or_city} ({formatted_date}).").add_break()
            if notes !="nan":
                comment = p.add_run(notes)
                print(notes)
                comment.font.bold = True
                # comment.font.underline = True
                comment.font.color.rgb = RGBColor.from_string("B10026")
                comment.add_break()

def make_press_list(press_csv):
    pass ##########



LANG = "" # English    
# LANG = "_JP" # Japanese
doc = Document(f"../templates/CV_Template{LANG}.docx")
make_publication_list(f"../achievements/Publications.csv", separate_reviews=True)
make_presentation_list(f"../achievements/Presentations{LANG}.csv")
make_funding_list(f"../achievements/Funding{LANG}.csv")
make_patent_list(f"../achievements/Patents{LANG}.csv")
make_award_list(f"../achievements/Awards{LANG}.csv")
# make_others_list("Others.csv")
make_press_list("../achievements/Press.csv")
doc.save(f"../achievements/Ooka_CV{LANG}_draft.docx")
#### To do list:
# After outputting the docs, the 1ページの行数を指定時に文字をグリッド線に合わせる needs to be unchecked (Ctrl + A).
# 年度
# Needs Japanese mode in general

