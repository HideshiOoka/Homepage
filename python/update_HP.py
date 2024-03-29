#%%
from update_publications import write_publications_html
from update_presentations import write_presentations_html
from CV_utils import write_csv_from_bib
from clean_bib import save_cleaned_bib

write_csv_from_bib("../achievements/Publications.bib")       
save_cleaned_bib()
for LANG in ["","_JP"]:
    write_presentations_html(LANG)
    write_publications_html(LANG)
