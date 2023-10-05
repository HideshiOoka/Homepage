#%%
import pypdf
import glob
merger = pypdf.PdfMerger()

base_dir = "C:/usr/Research/Funding/2023_Assc_Prof/20230930_Hyogo_Pref_U_Assc_Prof_Appl_Chem/"
file_list = glob.glob(base_dir + "to_merge/*")
print(file_list)

for i, file in enumerate(file_list):
    merger.append(file)
merger.write(base_dir + "merged_file.pdf")
merger.close()