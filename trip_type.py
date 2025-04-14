import pandas as pd
import re

# Provided metadata
update_time = "2025/03/31"
event_date = "2025/3/26"
event_time = ""
event_type = "Trip"
broker_name = "UBS"
event_name = "上海国际半导体展实地调研"

# Provided email content
email_content = """
PRELIM SCHEDULE – as of 20250321
      Wednesday, 26 Mar – Shanghai
Corporate meetings会议室管理层交流 - 梅花路1108号证大喜马拉雅酒店二楼会议室 - 惠厅：
•	Accotest (Huafeng Test & Control) 华峰测控 (688200.SH) - Confirmed
•	Wanye 万业企业 (600641.SH) – Confirmed
•	Konfoong Materials 江丰电子(300666.SZ) - Confirmed
•	AMEC 中微公司 (688012.SH) - Confirmed
•	Beijing Jingyi Automation京仪装备  (688652.SH) – Confirmed
•	Expert meeting 国内半导体设备材料投资基金合伙人– Confirmed
•	Piotech 拓荆科技 (688072.SH) – Confirmed
•	JHT 金海通 (603061.SH) –Confirmed

Thursday, 27 Mar – Shanghai
UBS Guided tour of SEMICON Exhibition展台参观及管理层/IR交流： 
•	AMEC 中微公司(688012.SH) – TBD
•	JEOL (6951.T) – Confirmed space limited 20ppls
•	Ushio (6925.T) – TBD
•	K&S (KLIC.O) – Confirmed 
•	KINGSEMI芯源微(688037.SH) – Confirmed
•	Sprint Precision先锋精科 (688605.SH) – Confirmed
•	Qingyi Photomask 清溢光电 (688138.SH) – Tent. Confirmed 
•	ACMR盛美半导体 (ACMR.O) / Huaqing华海清科(688120.SH) / Hangzhou Changchuan长川 (300604.SZ) – TBD
Corporate meetings会议室管理层交流 - 梅花路1108号证大喜马拉雅酒店二楼会议室 – 儒2厅：
•	Leadmicro Nano微导纳米 (688147.SH)  – Confirmed
•	NAURA Technology北方华创(002371.SZ) – Confirmed
•	Expert meeting- Litho专家 – Confirmed

Friday, 28 Mar – Shanghai
UBS Guided tour of Semicon Exhibition展台参观及管理层/IR 交流： 
•	Fortrune Precision富创精密 (688409.SH) – Confirmed
•	SICC天岳先进 (688234) – Confirmed
•	Injet Electric英杰电气 (300820.SZ) –Confirmed
•	Gentech正帆科技 (688596.SH) – Confirmed
•	PNC Process 至纯科技 (603690.SH) – Confirmed
"""

# Regex pattern to extract tickers
pattern = r"\((\w+\.\w+|\d{6})\)"

# Extract tickers
tickers = re.findall(pattern, email_content)

# Create the table
data = {
    "update time": [update_time] * len(tickers),
    "event date": [event_date] * len(tickers),
    "event time": [event_time] * len(tickers),
    "event type": [event_type] * len(tickers),
    "broker name": [broker_name] * len(tickers),
    "event name": [event_name] * len(tickers),
    "ticker": tickers
}

df = pd.DataFrame(data)
import ace_tools as tools; tools.display_dataframe_to_user(name="Event Ticker Table", dataframe=df)

