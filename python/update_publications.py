#%%
import pandas as pd
translate_dict = {"Scientific Publications":"論文",
                  "Corresponding Author":"責任著者",
                  "First Author":"筆頭著者",
                  "Last Author":"最終著者",
                  "Patents":"知財・特許"}    
def format_title(title):
    return title.replace(";",",")
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
def translate(txt):
    for k,v in translate_dict.items():
        txt = txt.replace(k,v)
    return txt   
for LANG in ["","_JP"]:
    #### Main Articles #####
    publications = pd.read_csv(f"../achievements/Publications.csv", index_col = 0) # {LANG}
    publications = publications.sort_values(by = ["status"]).iloc[::-1]
    # The 2 step sort is done to prioritize empty status (=accepted) articles in the order
    publications = publications.sort_values(by = ["type","year"], ascending = [True, False]).fillna("")
    original = publications[publications["type"]=="Original"]
    review = publications[publications["type"]=="Review"]
    editorial = publications[publications["type"]=="Editorial"]


    num_corresponding = publications["author"].str.contains("Ooka*").sum() 
    num_first = publications["ID"].str.contains("Ooka").sum()
    out_html = f"(Corresponding Author: {num_corresponding}, First Author: {num_first})<br>\n\n"

    df_list =[original, review, editorial]
    for i, df in enumerate(df_list):
        if i == 0:
            out_html += f"\n\t<h2>Original Articles</h2><ol>\n"
        elif i == 1:
            out_html += f"\n\t<h2>Reviews</h2><ol>\n"
        elif i == 2:
            out_html += f"\n\t<h2>Editorials and Perspectives</h2><ol>\n"
        year_header = 2030
        N = df.shape[0]
        for j in range(N):
            data = df.iloc[j]# .astype(str)
            type,notes,status,url,preprint,bib_key,j_key,title,pages,volume,year,fullname,abbrv,journal,authors,ENTRYTYPE,ID  = data
            year = int(year)
            if year < year_header:
                year_header = year
                out_html += f"\t<h2>{year_header}</h2>\n"
            if authors != "":
                authors = format_authors(authors)
                out_html += f"\t\t<li>{authors}"
            if title != "":
                out_html += f" <b>\"{title}\"</b>" 
            if journal != "":
                out_html += f", <i>{journal}</i>"
            if year != "":
                out_html += f", <b>{year}</b>"
            if volume != "":
                volume = int(volume)
                out_html += f", <i>{volume}</i>"
            if pages != "": 
                out_html += f", {pages}"
            if status != "":
                out_html += f" (<i>{status}</i>)"
            out_html += "."
            if url != "":
                out_html += f"    <a href=\"{url}\" target=\"_blank\">link</a>"
            if preprint != "":
                out_html += f"    <a href=\"{preprint}\" target=\"_blank\">preprint</a>"            
            out_html += f"<br>\n\n" 
        out_html += "\t</ol>\n\n"
    #### Other Articles (Non Peer Reviewed) #####
    out_html += f"<h2>Other Articles (Non Peer Reviewed)</h2><ol>\n"
    df = pd.read_csv(f"../achievements/Non_Peer_Reviewed{LANG}.csv")
    df = df.sort_values(by = ["Date"], ascending = [False]).fillna("")
    N = df.shape[0]
    for i in range(N):
        data = df.iloc[i].astype(str)
        title, authors, journal, year, volume, pages, URL, type, date, doi, notes = data
        year = int(year)
        volume = int(volume)

        title = format_title(title)
        authors = format_authors(authors)
        if pages != "": # it has "proper" bibliography information:
            out_html += f"\t\t<li>{authors} \"{title}\", <i>{journal}</i>, <b>{year}</b>, <i>{volume}</i>, {pages}.<br>\n\n"
        if pages == "": # it must have a URL
            out_html += f"\t\t<li>{authors} \"{title}\", <i>{journal}</i> (<a href={URL}>URL</a>).<br>\n\n"
    out_html += "\t</ol>\n\n"



    out_html = out_html.replace("MoS$_2$", "MoS<sub>2</sub>").replace("CO$_2$", "CO<sub>2</sub>").replace("{\`e}","&egrave").replace("MnO$_2$", "MnO<sub>2</sub>")
    out_html = out_html.replace("--"," - ")
    out_html = out_html.replace("<i></i>, ","").replace(", .", ".")

    if LANG == "_JP":
        out_html = translate(out_html)

    with open(f"../publications{LANG}.html", "r", encoding="utf-8") as f:
        original_html = f.read()
        original_contents = original_html.split("<!-- PAGE SPECIFICS -->")[1].split("<!-- END PAGE SPECIFICS-->")[0]
        # print(original_contents[6000:])
    with open(f"../publications{LANG}.html", "w", encoding="utf-8") as f:
        new_html = original_html.replace(original_contents, out_html)
        f.write(new_html)
