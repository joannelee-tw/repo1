import requests
import pandas as pd

description_ref = 'https://www.sec.gov/Archives/edgar/lookup-data.js?version=2.0'
import requests
import re
import json


"""
Get description mapping data
"""
# URL for the JS file (you might need to confirm this exact URL from the browser)
url = "https://www.sec.gov/Archives/edgar/lookup-data.js?version=2.0"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://www.sec.gov/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Success!")
    js_content = response.text
    secLookupData = js_content.split("const secLookupData = ")[1]

    if secLookupData:

        try:
            sec_lookup_data = json.loads(secLookupData)

            # Step 4: Process submissionForms mapping
            submission_forms = sec_lookup_data['submissionForms']
            form_description_mapping = {}

            for form_code, value in submission_forms.items():
                parts = value.split('|')
                description = parts[2].strip() if len(parts) > 2 else ""
                form_description_mapping[form_code] = description

            """
            # Step 5: Example output
            for k in list(form_description_mapping.keys())[:10]:
                print(f"{k}: {form_description_mapping[k]}")
            """

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("Could not find JSON object in JS file.")
else:
    print(f"Failed. Status Code: {response.status_code}")




"""
Get filing data
"""
class GetFilingData():
    def __init__(self, CIK, description_mapper):
        self.CIK = CIK
        self.json_url = f'https://data.sec.gov/submissions/CIK{CIK}.json'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }

    def get_filing_data(self):

        self.get_json()
        self.map_description()
        self.generate_url()

        df = pd.DataFrame(self.recent_filings)
        return df


    def get_json(self):
        """
        Crawl json filing data
        """
        response = requests.get(self.json_url, headers = self.headers)

        if response.status_code == 200:
            data = response.json()  # Parse JSON content
            # Example: Print basic info
            print("CIK:", data.get("cik"))
            print("Entity Name:", data.get("name"))
            self.recent_filings = data.get("filings", {}).get("recent", {})
        else:
            print("Failed to fetch data. Status code:", response.status_code)


    def map_description(self):
        """
        Map description to filing data based on form
        """
        self.recent_filings["form_description"] = []

        for form in self.recent_filings["form"]:
            if form[-2:] == "/A":
                form_org = form[:-2]
                description = form_description_mapping[form_org] + " - amendment"
            else:
                description = form_description_mapping[form]
            
            self.recent_filings["form_description"].append(description)

    def generate_url(self):
        self.recent_filings["filing_url"] = []

        for accession_num, primary_doc in zip(self.recent_filings["accessionNumber"], self.recent_filings["primaryDocument"]):
            self.recent_filings["filing_url"].append(self.get_url(accession_num, primary_doc))


    def get_url(self, accession_num, primary_doc):
        url = "/".join(["https://www.sec.gov/Archives/edgar/data", self.CIK[4:], "".join(accession_num.split("-")), primary_doc])
        return url




eik = "0000320193"

filing_obj = GetFilingData(eik, form_description_mapping)
df = filing_obj.get_filing_data()
df.to_excel("test_2.xlsx")
