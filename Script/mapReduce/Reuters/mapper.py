import sys
from bs4 import BeautifulSoup


#with open('reuters-sgm/reut2-000.sgm', 'r') as f:
#    # Se usa formato HTML para manejo de etiquetas
#    data = BeautifulSoup(f, 'html.parser')
#    for titles in data.find_all('title'):
#        print(titles.text)

for lines in sys.stdin:
    print(lines)
    soup = BeautifulSoup(lines, "html.parser")
    title = soup.find('title')
    if title:
        print(title.text)
    else:
        print('NOT FOUND')
    
