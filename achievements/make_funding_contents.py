#%%
import pandas as pd
def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date

def formatted_notes(notes):
    if notes == "":
        return ""
    else:
        return f" ({notes})"
    


for LANG in ["","_JP"]:
    df = pd.read_csv(f"Funding{LANG}.csv")
    out_html = "<h1>Funding</h1>"
    df = df.sort_values(by = "Start", ascending = False).fillna("")
    N = df.shape[0]

    out_html += f"\n\t<ol>\n"
    for i in range(N):
        data = df.iloc[i].astype(str)
        start,finish,title,name,funding_source,PI,amount,unit = data
        
        
        out_html += f'\t\t<li><b>{name}</b> "{title}" ({PI}), {amount} {unit} ({start}--{finish}).</li><br>\n\n'
    out_html += "\t</ol>\n\n"
    with open(f"../contents/funding{LANG}_contents.html", "w") as f:
        f.write(out_html)
        
