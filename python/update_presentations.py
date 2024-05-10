#%%
import pandas as pd
from update_date import update_date
from formatting import format_date
import datetime


format_list = ["Upcoming Presentations","Invited","Oral","Poster"]
all_df = pd.read_csv("../achievements/Presentations.csv")
today = int(datetime.date.today().strftime("%Y%m%d"))

def presentation_df_to_html(df, out_html, format):
    df = df.sort_values(by = "Date", ascending = False)
    N = df.shape[0]
    out_html += f"\t<h2>{format} ({N})</h2>\n\t<ol>\n"
    for i in range(N):
        data = df.iloc[i].astype(str)
        date,conference,venue,country_or_city,title,authors,format,notes = data
        date = format_date(date)
        out_html += f'\t\t<li>{authors}, <b>"{title}"</b>, {conference}, {venue}, {country_or_city} ({date}).</li><br>\n\n'
    out_html += "\t</ol>\n\n"
    return out_html

def write_presentations_html(LANG):
    out_html = ""
    for j,format in enumerate(format_list):
        if format == "Upcoming Presentations":
            df = all_df[all_df.Date >= today]
        else:
            df = all_df[all_df.Date < today]
            df = df[df.Format == format_list[j]]
        out_html = presentation_df_to_html(df, out_html, format)
            
    with open(f"../presentations{LANG}.html", "r", encoding="utf-8") as f:
        original_html = f.read()
        original_contents = original_html.split("<!-- PAGE SPECIFICS -->\n")[1].split("<!-- END PAGE SPECIFICS-->")[0]
    with open(f"../presentations{LANG}.html", "w", encoding="utf-8") as f:
        new_html = original_html.replace(original_contents, out_html)
        new_html = update_date(new_html)
        f.write(new_html)