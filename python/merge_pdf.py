#%%
import pypdf
import glob
merger = pypdf.PdfMerger()
#%%
base_dir = "C:/usr/Research/Funding/2023_Assc_Prof/20230930_Hyogo_Pref_U_Assc_Prof_Appl_Chem/"
file_list = glob.glob(base_dir + "to_merge/*")
print(file_list)

for i, file in enumerate(file_list):
    merger.append(file)
merger.write(base_dir + "merged_file.pdf")
merger.close()

#%%

from pypdf import PdfReader, PdfWriter
file = "c:/Users/ohflu/Downloads/Polovtsian_Act_2.pdf"
pdf_writer = PdfWriter()  # we want to reset this when starting a new pdf
pdf_reader = PdfReader(file)
pages = (138, 207)


for idx in range(pages[0] - 1, pages[1]):
    pdf_writer.add_page(pdf_reader.pages[idx])
output_filename = file.replace(".pdf","extracted.pdf")
with open(output_filename, "wb") as out:
    pdf_writer.write(out)
