#%%
from docx import Document
from docx.shared import Pt
doc = Document(r"C:\Users\Hideshi_Ooka\Research\Applications\___Archived\20200302_CV_Ooka.docx")
doc = Document("CV_template.docx")
pars = doc.paragraphs

items = ["Heading", "Publications", "Presentations","Patents","Press"]
for item in items:
    doc.add_paragraph(item,style = "Heading 1")

doc.save("CV.docx")
