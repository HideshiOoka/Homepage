#%%
import pandas as pd
import bibtexparser

def write_csv_from_bib(bib_file, sort = True):
    with open(bib_file) as f:
        bib = bibtexparser.load(f)
    df = pd.DataFrame(bib.entries)    
    cols = ["ID", "author","journal","year","volume","pages", "doi", "notes", "ENTRYTYPE"]
    missing_cols = [item for item in df.columns if item not in cols]
    cols += missing_cols
    df = df[cols].sort_values(by=["year"], ascending = False)   
    df = df.fillna("")
    num_publications =df.shape[0]
    corresponding_authors = df.author.str.contains("Ooka\*").sum()
    first_authors = df.ID.str.contains("Ooka").sum()
    print(num_publications, corresponding_authors, first_authors)
    df.to_csv("../achievements/Publications.csv")
if __name__ == "__main__":
    write_csv_from_bib("../achievements/Publications.bib")
