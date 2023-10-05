#%%
import pandas as pd
def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date

def format_authors(authors):
    sorted_authors = ""
    for a in authors.split(" and "):
        try:
            last,first  = a.split(", ")
            sorted_authors += first + " " + last + ", "
        except ValueError:
            sorted_authors += a + ", "
    sorted_authors = sorted_authors[:-2]        
    return sorted_authors

for LANG in ["","_JP"]:
    df = pd.read_csv(f"Patents{LANG}.csv")
    out_html = "<h1>Patents</h1>"
    df = df.sort_values(by = "Date", ascending = False).fillna("")
    N = df.shape[0]

    out_html += f"\n\t<ol>\n"
    for i in range(N):
        data = df.iloc[i].astype(str)
        date, status, authors, title, ID = data
        date = format_date(date)
        authors = format_authors(authors)
        out_html += f'\t\t<li>{authors} <b>"{title}"</b> ID: {ID} ({date}, {status}).</li><br>\n\n'
    out_html += "\t</ol>\n\n"
    with open(f"../contents/patents{LANG}_contents.html", "w") as f:
        f.write(out_html)
