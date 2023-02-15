#%%
import pandas as pd

from docx import Document
LANG = 1 # English:0 or Japanese:1
# from docx.shared import Pt

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
        p.add_run(format(title))
        return p
    else:
        # break the runs? or do somethign?# # CO2, MoS2        
        p.add_run(format(title))
        return p

def make_publication_list(bib):
    with open(bib, encoding = "UTF-8") as f:
        bib_data = f.read().replace("\n", "")
    entries = bib_data.split("@")[1:]
    num_publications =len(entries)
    corresponding_authors = str(bib_data.count("Ooka*"))
    first_authors = str(bib_data.count("@article{Ooka"))
    out_txt = ""
    for i, entry in enumerate(entries):
        authors = entry.split("author = {")[1].split("},")[0]
        authors = sort(authors)
        journal = entry.split("journal = {")[1].split("},   ")[0]
        year = entry.split("year = {")[1].split("},   ")[0]
        volume = entry.split("volume = {")[1].split("},   ")[0]
        pages = entry.split("pages = {")[1].split("},   ")[0].replace("--","-")
        title = entry.split("title = {")[1].split("}}")[0]
        i+=1
        p = doc.add_paragraph(f"{i}.  ")
        p.add_run(authors)
        p.add_run(" \"")
        p = add_formatted_title(p,title) 
        p.add_run("\", ")
        p.add_run(journal).italic = True
        p.add_run(", ")
        p.add_run(year).bold = True
        p.add_run(", ")
        p.add_run(pages)
        p.add_run(".").add_break()
def make_funding_list(funding_csv):
    df = pd.read_csv(funding_csv)
    N = df.shape[0]
    titles =df["Title_JP"]
    names = df["PJ_Name_JP"]
    sources = df["Funding_Source_JP"]
    amounts = df["Amount"]
    units = df["Unit"]
    for i in range(N):
        data = df.iloc[i]
        start,finish,title, name, source, PI, amount, unit = data[["Start","Finish","Title_JP","PJ_Name_JP","Funding_Source_JP","PI","Amount","Unit"]]
        i+=1
        p = doc.add_paragraph("")
        if PI == "PI":
            PI = "(研究代表者)"
        else:
            PI = "(研究分担者)"    
        p.add_run(f"{i}.  {source} {name} {PI}\n").bold = True
        p.add_run(f"課題名：{title}\n")
        p.add_run(f"研究期間：{start} - {finish}\n")
        p.add_run(f"研究費総額：{amount}円").add_break()
        # funding amount with comma?
items = ["Heading", "Publications", "Presentations","Patents","Press","Funding","Awards"]
doc = Document("CV_template.docx")
    

for item in items:
    doc.add_paragraph(item,style = "Heading 1")
make_publication_list("Publications.bib")
make_funding_list("Funding.csv")


doc.save("CV.docx")
