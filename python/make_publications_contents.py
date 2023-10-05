#%%
import pandas as pd
translate_dict = {"Scientific Publications":"論文",
                  "Corresponding Author":"責任著者",
                  "First Author":"筆頭著者",
                  "Last Author":"最終著者",
                  "Patents":"知財・特許"}    

def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date


def format_authors(authors):
    formatted_authors = ""
    for a in authors.split(" and "):
        last,first  = a.split(", ")
        formatted_authors += first + " " + last + ", "
    formatted_authors = formatted_authors[:-2]        
    return formatted_authors

def translate(txt):
    for k,v in translate_dict.items():
        print(k,v)
        txt = txt.replace(k,v)
    return txt   

for LANG in ["","_JP"]:
    df = pd.read_csv(f"../achievements/Publications.csv", index_col = 0) # {LANG}
    df = df.sort_values(by = ["type","year"], ascending = [True, False]).fillna("")
    N = df.shape[0]
    num_original = df[df["type"]=="original"].shape[0]
    num_corresponding = df["author"].str.contains("Ooka*").sum() 
    num_first = df["ID"].str.contains("Ooka").sum()
    out_html = f"<h1>Publications</h1><br>\n(Corresponding Author: {num_corresponding}, First Author: {num_first})<br>\n\n"

    out_html += f"\n\t<h2>Original Articles</h2><ol>\n"
    year_header = "2030"

    
    for i in range(N):
        data = df.iloc[i].astype(str)
        ID, authors, journal, year, volume, pages, doi, notes, ENTRYTYPE, type, title, fullame, abbrv, status  = data
        if year < year_header:
            year_header = year
            out_html += "\t<h2>{}</h2>\n".format(year_header)
        authors = format_authors(authors)
        if pages == "": # must be not accepted yet
            volume = status
            pages = doi

        out_html += f"\t\t<li>{authors} \"{title}\", <i>{journal}</i>, <b>{year}</b>, <i>{volume}</i>, {pages}.<br>\n\n"

        if i == num_original-1:
            out_html += "\t</ol>\n\n"
            out_html += f"<h2>Review Articles</h2><ol>\n"
            

    out_html = out_html.replace("MoS$_2$", "MoS<sub>2</sub>").replace("CO$_2$", "CO<sub>2</sub>").replace("{\`e}","&egrave").replace("MnO$_2$", "MnO<sub>2</sub>")
    out_html += "\t</ol>\n\n"
    if LANG == "_JP":
        out_html = translate(out_html)
    with open(f"../contents/publications{LANG}_contents.html", "w", encoding="utf-8") as f:
        f.write(out_html)
