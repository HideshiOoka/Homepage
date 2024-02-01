#%%	
import datetime
import re

def update_date(html):
    today = datetime.date.today().strftime('%Y/%m/%d')
    # html = re.sub("\d\d\d\d/\d\d/\d\d", today, html, count=0, flags=0)    
    k = html.rfind("\d\d\d\d/\d\d/\d\d")
    new_string = html[:k] + today + html[k+1:]
    return html



