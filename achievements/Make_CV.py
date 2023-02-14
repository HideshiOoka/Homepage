#%%
from docx import Document
LANG = 0 # English:0 or Japanese:1
# from docx.shared import Pt

def sort(authors):
    sorted_authors = ""
    for a in authors.split(" and "):
        last,first  = a.split(", ")
        sorted_authors += first + " " + last + ", "
    sorted_authors = sorted_authors[:-2]        
    return sorted_authors

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
        p.add_run(title)
        p.add_run("\", ")
        p.add_run(journal).italic = True
        p.add_run(", ")
        p.add_run(year).bold = True
        p.add_run(", ")
        p.add_run(pages)
        p.add_run(".").add_break()
    # -- in SPET
    # # CO2, MoS2        



items = ["Heading", "Publications", "Presentations","Patents","Press","Funding","Awards"]
doc = Document("CV_template.docx")


for item in items:
    doc.add_paragraph(item,style = "Heading 1")
make_publication_list("Publications.bib")
doc.save("CV.docx")
