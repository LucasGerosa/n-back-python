import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from defaults import *

'''Modified from  https://github.com/pranav7712/OFFICE_AUTOMATION'''

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
input_folder = f'{ROOT_DIR}/../input'


def extract_url_file(input_url,folder_path=os.getcwd(), extension = '.pdf'):
    
    import os
    import requests
    from urllib.parse import urljoin
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime

    #If there is no such folder, the script will create one automatically
    folder_location = folder_path
    if not os.path.exists(folder_location):os.makedirs(folder_location)

    response = requests.get(input_url)
    soup= BeautifulSoup(response.text, "html.parser") 

    link_text=list()
    link_href=list()
    link_file=list()
    
    counter=0

    for link in soup.select(f"a[href$='{extension}']"):
        #Name the pdf files using the last portion of each link which are unique in this case
        filename = os.path.join(folder_location,link['href'].split('/')[-1])
        if DEFAULT_INTENSITY in filename and not 'mono' in filename:
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(input_url,link['href'])).content)
                
            link_text.append(str(link.text))
            
            link_href.append(link['href'])

            link_file.append(link['href'].split('/')[-1])
            
            counter+=1

            print(counter, "-Files Extracted from URL named ",link['href'].split('/')[-1])
        
    table_dict={"Text":link_text,"Url_Link":link_href,"File Name":link_file}

    df=pd.DataFrame(table_dict)
    
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    
    '''
    print("Creating an Excel file with Name of FIle, Url Link and Link Text...")

    new_excel_file=os.path.join(folder_location,"Excel_Output_"+time_stamp+".xlsx")

    writer = pd.ExcelWriter(new_excel_file, engine='openpyxl')

    df.to_excel(writer,sheet_name="Output")

    writer.save()
    '''
    print(f"All {extension} files downloaded.")
    
def extract_url_from_instrument(instrument:str, extension:str='aiff'):
    base_url = 'https://theremin.music.uiowa.edu/MIS'
    input_url = f'{base_url}{instrument}.html'
    extension = '.' + extension
    directory = f'{input_folder}/{instrument}/aiff'
    extract_url_file(input_url, directory, extension)

def download_all() -> None:
    extract_url_from_instrument('piano')
    extract_url_from_instrument('guitar', 'aif')

    


    
