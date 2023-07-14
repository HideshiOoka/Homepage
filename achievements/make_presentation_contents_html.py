#%%
import pandas as pd
def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date


all_df = pd.read_csv("Presentations.csv")



format_list = ["Invited","Oral","Poster"]
out_html = "<h1>Presentations</h1>"
for j,format in enumerate(format_list):
    df = all_df[all_df["Format"] == format_list[j]]
    df = df.sort_values(by = "Date", ascending = False)
    N = df.shape[0]

    out_html += f"\t<h2>{format} ({N})</h2>\n\t<ol>"
    for i in range(N):
        data = df.iloc[i].astype(str)
        date,conference,venue,country_or_city,title,authors,format,notes = data[:8]
        date = format_date(date)
        out_html += f'<li>{authors}, <b>"{title}"</b>, {conference}, {venue}, {country_or_city} ({date}).</li>'
    out_html += "\t</ol>\n\n"
with open("../contents/presentations_contents.html", "w") as f:
    f.write(out_html)
#%%



    doc.add_heading("Presentations (Japanese Titles were Translated to English)", level=1)
    for j,df in enumerate(format_list):

        doc.add_heading(format_list[j] + " Presentations"+f" ({N})", level=2)
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


#Date,Conference,Venue,Country_or_City,Title,Authors,Format,Notes,Conference_JP,Venue_JP,Country_or_City_JP,Title_JP,