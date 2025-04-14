# -*- coding: utf-8 -*-
'''
使用說明:
直接從skype 簽到處複製對話框  如下面
上午 08:30
20241212
0830 in
下午 12:04
20241212
1200 out

Erica，上午 08:29
20241213
0827 in


Erica，下午 05:34
20241213
1734 out

複製出來會長這樣 自己的名字會消失 需手動補上 長得跟其他人一樣就好 空行不管 下面是補完的樣子

Robert，上午 08:30
20241212
0830 in
Robert，下午 12:04
20241212
1200 out

Erica，上午 08:29
20241213
0827 in


Erica，下午 05:34
20241213
1734 out

把資料存到一個txt 改TXT路徑到自己那 Name list 修改成所有pt的名字就可以 會自動生成當月Excel
(我幾乎沒考慮例外條件 如果有兩個pt一樣名字就會爆掉XD)
'''

'''
Teams 的複製方式 (單純Ctrl+C 人名會消失)
1. 滑鼠點選群組內任何位置
2. Ctrl + A
3. 上滑至開始複製的日期(直到第一則要複製的訊息出現在螢幕上)
4. Ctrl + C
5. 到記事本(.txt) Ctrl + V
6. 刪除前後非聊天紀錄的文字 (會複製一些Teams的功能文字，也會複製到最新的以及前幾則上個月的簽到訊息，這些都要刪掉)

最後的.txt檔案應該會長這樣 (會包含自己的名字，所以不用補) :

============================
由 Erica Ye 的 訊息
Erica Ye


20250328
1747 out
今天 上午 08:22
由 Robert Chen 的 訊息
Robert Chen


20250331
0820 in
由 Thomas Hsu 的 訊息
Thomas Hsu


20250331
0821 in
由 Joanne Lee 的 20250331 0843 in
Joanne Lee

20250331
0843 in

今天 下午 12:34
由 Robert Chen 的 訊息
Robert Chen


20250331
1200 out
=========================================
'''

# -*- coding: utf-8 -*-
import os
import shutil
import pandas as pd
from datetime import datetime
from openpyxl.styles import Alignment
from openpyxl import load_workbook

BASE_PATH = r"Z:\08_Tarobo\7. 個人\Miao\簽到"
TXT_PATH = r"C:\Users\joannelee\Desktop\test.txt"
NAME_LIST = ['Erica', 'Robert', 'Thomas', 'Joanne']


def find_max_date_file():
    filenames = os.listdir(BASE_PATH)
    filedates = []

    for filename in filenames:
        if 'PT簽到表' in filename and filename.endswith('.xlsx'):
            try:
                filedate = filename.split('_')[1].split('.')[0]
                if len(filedate) == 6:
                    filedate = datetime.strptime(filedate, '%Y%m')
                    filedates.append(filedate)
            except Exception:
                continue

    if not filedates:
        print("錯誤：未找到符合的 Excel 檔案")
        return None

    max_date = max(filedates)
    print(max_date)

    return max_date.strftime('%Y%m')

def get_new_file_path():
    new_date = datetime.today().strftime('%Y%m')
    new_file_name = f"PT簽到表_{new_date}.xlsx"
    new_path = os.path.join(BASE_PATH, new_file_name)

    return new_date, new_file_name, new_path

def copy_and_rename_excel():
    new_date, new_file_name, new_path = get_new_file_path()

    if os.path.exists(new_path):
        print(f"檔案已存在，直接修改：{new_path}")
        return new_path
    
    old_date = find_max_date_file()
    if not old_date:
        return None
    
    old_excel = f'PT簽到表_{old_date}.xlsx'
    old_path = os.path.join(BASE_PATH, old_excel)
    print(old_path)

    if not os.path.exists(old_path):
        print(f"錯誤：找不到原始檔案 {old_path}")
        return None

    shutil.copy2(old_path, new_path)
    print(f"檔案已成功複製並重新命名為：{new_date}")

    return new_path

# 讀取 TXT 檔案並轉換為 DataFrame
def load_sign_data(txt_path):
    name, date, time, action = [], [], [], []

    with open(txt_path, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    filtered_lst = [x.strip() for x in all_lines if x.strip()]

    for idx in range(len(filtered_lst)):
        if idx % 3 == 0:
            name.append(filtered_lst[idx].split('，')[0])
        elif idx % 3 == 1:
            date.append(filtered_lst[idx])
        elif idx % 3 == 2:
            string_split = filtered_lst[idx].split(' ')
            time.append(string_split[0])
            action.append(string_split[1])

    date = [f"{d[:4]}/{d[4:6]}/{d[6:]}" for d in date]
    time = [f"{t[:2]}:{t[2:]}" for t in time]

    return pd.DataFrame({'name': name, 'date': date, 'time': time, 'action': action})


# 讀取 TXT 檔案並轉換為 DataFrame  (Teams 版本)
def load_sign_data_teams(txt_path):
    name, date, time, action = [], [], [], []

    with open(txt_path, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    filtered_lst = [x.strip() for x in all_lines if x.strip()]

    step_no = 0 #1: Name coming up / 2: Date coming up / 3: time and status coming up
    for idx in range(len(filtered_lst)):
        if step_no ==1: #Name
            if any (name in filtered_lst[idx] for name in NAME_LIST) and '由' not in filtered_lst[idx]:
                name.append(filtered_lst[idx].split(' ')[0])
                step_no += 1
        elif step_no == 2: #date
            try: 
                int(filtered_lst[idx])
                date.append(filtered_lst[idx])
                step_no += 1
            except:
                pass

        elif step_no == 3: #in/out time
            if 'in' not in filtered_lst[idx] and 'out' not in filtered_lst[idx]:
                pass
            else:
                string_split = filtered_lst[idx].split(' ')
                time.append(string_split[0])
                action.append(string_split[1])
                step_no = 0 
        elif '由' in filtered_lst[idx]: 
            step_no = 1



    date = [f"{d[:4]}/{d[4:6]}/{d[6:]}" for d in date]
    time = [f"{t[:2]}:{t[2:]}" for t in time]


    reference_start = datetime(2025, month-1, 26)
    reference_end = datetime(2025, month, 25)
    df = pd.DataFrame({'name': name, 'date': date, 'time': time, 'action': action})
    df["date_dtype"] = pd.to_datetime(df["date"], format="%Y/%m/%d")
    df_filtered = df[df["date_dtype"] <= reference_end]
    df_filtered = df_filtered[df_filtered["date_dtype"] >= reference_start]
    df_final = df_filtered.drop("date_dtype", axis = 1)
    return df_final

# 從 DataFrame 擷取符合條件的值
def sign(data, col, name, action):
    df_filtered = data[(data['name'] == name) & (data['action'] == action)]
    return df_filtered[col].tolist()

# 確保所有的 Sheet 存在且正確
def validate_sheets(wb):
    existing_sheets = wb.sheetnames
    sheets_to_keep = {}

    for sheet in existing_sheets:
        for name in NAME_LIST:
            if name in sheet:  
                sheets_to_keep[sheet] = name
                break

    # 如果沒有找到符合條件的 Sheet，則複製第一個 Sheet 作為模板
    for name in NAME_LIST:
        if not any(name in sheet for sheet in existing_sheets):
            print(f"找不到 '{name}'，正在創建新工作表...")
            new_sheet = wb.copy_worksheet(wb[wb.sheetnames[1]]) 
            new_sheet.title = name
            sheets_to_keep[name] = name

    # 刪除不在 Name List 中的 Sheet
    for sheet in existing_sheets:
        if sheet == '日期':
            continue
        if sheet not in sheets_to_keep:
            print(f"刪除無效工作表: {sheet}")
            del wb[sheet]

    return sheets_to_keep

def apply_conditions(sheet, row):
    time_in = sheet[f"C{row}"].value
    time_out = sheet[f"D{row}"].value

    if time_in and time_out:
        time_in_float = float(time_in.replace(":", "."))
        time_out_float = float(time_out.replace(":", "."))
        
        if time_out_float < 17.30 and time_out_float > 12.00:
            # 清空該員工的 Excel Sheet
            
            """for row_idx in range(3, 16):
                for col_idx in range(1, 7):  # A=1, B=2, ..., F=6
                    sheet.cell(row=row_idx, column=col_idx, value="")
            sheet[f"G3"] = f"錯誤: Row {row} 下班時間 {time_out} 早於 17:30，請檢查資料。"""
            print(f"警告：Row {row} 下班時間 {time_out} 早於 17:30，為甚麼這麼早下班?")
            #raise ValueError(f"Row {row}: 下班時間 {time_out} 早於 17:30，請檢查資料。")

        if 8.00 <= time_in_float <= 10.00 and 17.00 <= time_out_float <= 18.30:
            sheet[f"F{row}"] = -1

def update_salary(new_path, df):
    wb = load_workbook(new_path)
    valid_sheets = validate_sheets(wb)
    
    today = datetime.today()
    year = today.strftime('%Y')  
    month = today.strftime('%m')  

    target_sheet = None
    for sheet in wb.sheetnames:
        if "日期" in sheet:
            target_sheet = wb[sheet]
            target_sheet["C2"] = year
            target_sheet["C3"] = month

    for sheet_name, name in valid_sheets.items():
        target_sheet = wb[sheet_name]
        print(f"更新工作表：{sheet_name}")

        target_sheet["A1"].value = (
            f'="{name} 簽到表"&"  "&"("&"   "&日期!C2&"   "&"年"&"   "&日期!C3&"   "&"月"&")"'
        )

        for row in range(3, 16):
            for col in range(1, 7):
                target_sheet.cell(row=row, column=col, value="")

        date_list = sign(df, 'date', name, 'in')
        time_in_list = sign(df, 'time', name, 'in')
        time_out_list = sign(df, 'time', name, 'out')

        for i, date in enumerate(date_list):
            row = 3 + i
            target_sheet[f"A{row}"] = date
            target_sheet[f"B{row}"] = f'=RIGHT(TEXT(A{row},"[$-404]dddd"),1)'
            
            time_in = time_in_list[i] if i < len(time_in_list) else ""
            time_out = time_out_list[i] if i < len(time_out_list) else ""

            target_sheet[f"C{row}"] = time_in
            target_sheet[f"D{row}"] = time_out

            try:
                apply_conditions(target_sheet, row)
            except ValueError as e:
                print(f"錯誤處理：{e}")
                continue

        print(f"已完成 {name} 的資料更新")

    wb.save(new_path)
    wb.close()
    print("Excel 更新完成")


def main():
    # 執行流程
    #df_sign = load_sign_data(TXT_PATH) 

   
    df_sign = load_sign_data_teams(TXT_PATH) 
    new_file_path = copy_and_rename_excel()
    
    
    if os.path.exists(new_file_path):
        update_salary(new_file_path, df_sign)
    else:
        print(f"找不到 Excel 檔案：{new_file_path}")


if __name__ == '__main__':

    #config----------
    month = 4 #change to the desired month (affects the filtering of sign-in data in Teams)
    #config end -------------

    main()