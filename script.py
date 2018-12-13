import csv
from django.utils.encoding import smart_str
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

chromedriver = '/home/meet/Documents/george/chromedriver'
driver = webdriver.Chrome(chromedriver)

driver.get("https://selvbetjening.trafikstyrelsen.dk/Sider/resultater.aspx")
driver.maximize_window()
elem = driver.find_element_by_id("ctl00_m_g_6f9923c7_5864_4e71_bcd8_017cfab1946d_ctl00_ctl00_txtRegNo")
elem.send_keys('ah12712')
elem.send_keys(Keys.RETURN)

element = driver.page_source
soup = BeautifulSoup(element)

final_array = []
for table in soup.findAll('table',{'id':'tblInspections'}):
    for tbody in table.findAll('tbody'):
        for tr in tbody.findAll('tr'):
            temp = []
            for td in tr.findAll('td'):
                td_Text = smart_str(td.text)
                if td.findAll('span'):
                   for span in td.findAll('span'):
                        temp.append(smart_str(span.text))
                elif td.findAll('a'):
                    for link in td.findAll('a'):
                        temp.append(smart_str(link.get('href')))
                        break
                else:
                    temp.append(td_Text)
            final_array.append(temp)


for i in final_array:
    print i


outfile = open('Sample.csv', 'w')
writer = csv.writer(outfile)
writer.writerow(['Dato','Resultat','Km-stand','Reg.nr.','Gem'])
for row in final_array:
    writer.writerow(row)
outfile.close()
driver.close()

