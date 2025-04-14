import requests
import json
from bs4 import BeautifulSoup
import re

url = 'https://www.r-agent.com/kensaku/companydetail/02430/index2.html'
response = requests.get(url)

if response.status_code == 200:

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')

    script_tag = soup.find("script", string=re.compile("window\\.vueData"))
    script_content = script_tag.string

    #資料清理成JSON型式
    job_list = script_content.split("pageNo")[0].split(",\n    \n],\n      pankuzu")[0].split("jobofferList:")[1] + "]"
    job_list = re.sub(r'\s+', ' ', job_list.strip())
    j_list_formatted = re.sub(r'([{,]\s*)(\w+)(\s*:\s*)', r'\1"\2"\3', job_list).replace(", ]", "]")


    # Try to load the JSON to check for errors
    try:
        data = json.loads(j_list_formatted)
        with open("r_agent_jobs.json", "w", encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent = 2)
        
    except json.JSONDecodeError as e:
        print(e)


else:
    print(f"Response status code : {response.status_code}")




