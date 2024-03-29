#%%
import pandas as pd
from update_date import update_date
def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date

format_list = ["Invited","Oral","Poster"]
all_df = pd.read_csv("../achievements/Presentations.csv")


def write_presentations_html(LANG):
    out_html = "<h1>Presentations</h1>"
    for j,format in enumerate(format_list):
        df = all_df[all_df["Format"] == format_list[j]]
        df = df.sort_values(by = "Date", ascending = False)
        N = df.shape[0]

        out_html += f"\t<h2>{format} ({N})</h2>\n\t<ol>\n"
        for i in range(N):
            data = df.iloc[i].astype(str)
            date,conference,venue,country_or_city,title,authors,format,notes = data
            date = format_date(date)
            out_html += f'\t\t<li>{authors}, <b>"{title}"</b>, {conference}, {venue}, {country_or_city} ({date}).</li><br>\n\n'
        out_html += "\t</ol>\n\n"
    with open(f"../presentations{LANG}.html", "r", encoding="utf-8") as f:
        original_html = f.read()
        original_contents = original_html.split("<!-- PAGE SPECIFICS -->\n")[1].split("<!-- END PAGE SPECIFICS-->")[0]
        # print(original_contents[6000:])
    with open(f"../presentations{LANG}.html", "w", encoding="utf-8") as f:
        new_html = original_html.replace(original_contents, out_html)
        new_html = update_date(new_html)
        f.write(new_html)