import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import re
import lxml
import streamlit as st
import openpyxl
from openpyxl import Workbook
import numpy as np

c = {'ASP.NET_SessionId': 'uspd4czxuxtaiqokiilppwpf',
     '_gat': '1',
     '.AspNet.cpsAuth': 'CfDJ8GaK_vc8ictOkQAmLJSxb4QNGXklQcHQEGVvBsc_rKicZdF-XXkLQH4zUAzKjGKa83S9NZJTiWzKwtsN9G3LZ1W5Mfuqwa6fLisyXbWBK83518JQBYjOuiBMoNkGFUsxvBmJqWggeHyrCBXIU-BR6uxi5oMlZjQcaGFDPoQ1_-H7xZxdcbdmL92Ck62Wi7spacXKvviGoo_qkBzUqVXeMGoKQFKlLh3T-f66kKuZk5FeMOFCaIKdTnCIR4G-IywuxjUzGJPYl_OlnG8B-K00qd7K8nVbuwRnan2gHqnZyiB2xtAia6D4fE8-Ef8Auph5Ka1uFiOmjUbjtuCujUaQdXIxoKveaeeZuEYW49ky6ZpNVpSeoWgPlEXwH99YHf2yXHX9xqjtY1YGRlgyLgF0_hRcrjNSvD3uFb5VlwYS0qZT6anGvF4vN_PZuCZES32x50bm8ZfDebQFZyL3-euLBN3C7H0RzgyzeFqbEnTNCtd-JXpjKJgLbiZqOtQXYDsvJyckhESjlC8xXRwzaDnKWb_4fEJ68vp_v76kVSVLfLh0',
     'U2DA5BAE510384E938A713A1FB26F4236': 'CfDJ8GaK_vc8ictOkQAmLJSxb4QNGXklQcHQEGVvBsc_rKicZdF-XXkLQH4zUAzKjGKa83S9NZJTiWzKwtsN9G3LZ1W5Mfuqwa6fLisyXbWBK83518JQBYjOuiBMoNkGFUsxvBmJqWggeHyrCBXIU-BR6uxi5oMlZjQcaGFDPoQ1_-H7xZxdcbdmL92Ck62Wi7spacXKvviGoo_qkBzUqVXeMGoKQFKlLh3T-f66kKuZk5FeMOFCaIKdTnCIR4G-IywuxjUzGJPYl_OlnG8B-K00qd7K8nVbuwRnan2gHqnZyiB2xtAia6D4fE8-Ef8Auph5Ka1uFiOmjUbjtuCujUaQdXIxoKveaeeZuEYW49ky6ZpNVpSeoWgPlEXwH99YHf2yXHX9xqjtY1YGRlgyLgF0_hRcrjNSvD3uFb5VlwYS0qZT6anGvF4vN_PZuCZES32x50bm8ZfDebQFZyL3-euLBN3C7H0RzgyzeFqbEnTNCtd-JXpjKJgLbiZqOtQXYDsvJyckhESjlC8xXRwzaDnKWb_4fEJ68vp_v76kVSVLfLh0',
     '_ga': 'GA1.2.892393629.1661620881',
     '_gid': 'GA1.2.1909818050.1661620881'}
st.title('Get matches results')
but = st.button('Launch')
if but:
    res = requests.get('https://old.baltbet.ru/BetsTota.aspx?page=1', cookies=c)
    soup = BeautifulSoup(res.text, 'lxml')
    pag = soup.find('div', {'class': 'pages'})
    pag = pag.find_all('a')[1].text
    pag = int(pag)
    data = []
    for num in range(1, 3):  # pag+1
        st.write('Work with page number - ', num)
        res = requests.get('https://old.baltbet.ru/BetsTota.aspx?page={num}', cookies=c)
        soup = BeautifulSoup(res.text, 'lxml')
        list_1 = soup.find('table', {'class': 'totalmain'}).find_all('a')
        list_2 = ['https://old.baltbet.ru/' + i.get('href') for i in list_1]
        count = 0
        for l in list_2[:5]:
            count += 1
            print('Page - ', num, 'Work - ', l, 'count - ', count)
            res = requests.get(l, cookies=c)
            time.sleep(1.5)
            soup = BeautifulSoup(res.text, 'lxml')
            table = soup.find('table', {'class': 'betinfo2'})
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
    data_2 = []
    data = list(filter(None, data))
    data_1 = [j for i in data for j in i if len(j) == 1 or len(j) == 2]
    for i in data_1:
        data_2.append(i)
        data_2.append(' ')
    df = pd.DataFrame(data_2, columns=['Result'])
    df = df.T
    writer = pd.ExcelWriter('Result_list.xlsx')
    df.to_excel(writer, index=False)
    writer.save()
    st.write('Excel done')
    with open('Result_list.xlsx', "rb") as file:
        st.download_button(
            label="Download data as EXCEL",
            data=file,
            file_name=f'Result_list.xlsx',
            mime='text/xlsx',
        )

