import sys
sys.path.append(r"\\192.168.0.243\PublicDocs\08_Tarobo\7. 個人\PT_Code\Robo\PythonModule")
import SQLModule as SQLModule


def find_latest_date_for_item(cursor, table, column, item, initial_offset, max_offset, step):
    """
    Iteratively queries the table for the latest available date for the given item,
    starting from a specified initial offset from the current date and expanding the
    window (by subtracting additional days) until data is found or the maximum lookback is reached.
    
    Parameters:
        connection      : An open pyodbc connection.
        table           : Name of the table or view.
        column          : Column name to match (e.g., 'ticker' or 'code').
        item            : The specific ticker/code value to search for.
        initial_offset  : The starting day offset (e.g., -1 or -14).
        max_offset      : The maximum negative offset to look back (e.g., -30).
        step            : The decrement step (usually -1 to extend one day further).
    
    Returns:
        The latest available date (as returned by MAX(t_date)) for which data exists,
        or None if no data is found within the specified window.
    """
    current_offset = initial_offset
    while current_offset >= max_offset:
        query = f"""
            SELECT MAX(CAST(t_date as date)) AS latest_date
            FROM {table}
            WHERE {column} = ? 
              AND CAST(t_date as date) >= CAST(DATEADD(day, ?, GETDATE()) as date)
        """
        cursor.execute(query, (item, current_offset))
        result = cursor.fetchone()[0]
        if result is not None:
            return (result, current_offset)
        # Extend the search one more day back
        current_offset += step  
    return None

def get_latest_data_dates(cursor, max_lookback=-30):
    """
    Finds the latest available data dates for each country (ticker/code) by adjusting
    the query date in increments until data is found.
    
    Parameters:
        connection  : An open pyodbc connection to the SQL Server.
        max_lookback: The maximum day offset to look back (default is -30 days).
    
    Returns:
        A dictionary mapping each ticker/code to its latest available date.
    """
    latest_dates = {}
    
    # Define items for the first query ([QuantDB].[dbo].[i_qfii_other_flows])
    # with their starting offsets.
    tickers = {
        'KPCPNTFR Index': -1,
        'INBTFINT Index': -1,
        'JTBTFRN Index': -7,
        'BZSIFODN Index': -3,
    }
    
    for ticker, init_offset in tickers.items():
        latest_date = find_latest_date_for_item(
            cursor,
            "[QuantDB].[dbo].[i_qfii_other_flows]",
            "ticker",
            ticker,
            init_offset,
            max_lookback,
            -1
        )
        latest_dates[ticker] = latest_date
    
    # Define items for the second query (funddb view)
    codes = {
        'THIVNET$ Index': -1,
        'VNDXNET$ Index': -1,
        'MATPENET Index': -1,
    }
    
    for code, init_offset in codes.items():
        latest_date = find_latest_date_for_item(
            cursor,
            "funddb.dbo.v_fof_t_data_to_countryflow_qfii",
            "code",
            code,
            init_offset,
            max_lookback,
            -1
        )
        latest_dates[code] = latest_date
        
    return latest_dates

def get_newest_sql(latest:dict):
    current_sql = f"""
    select * 
    from [QuantDB].[dbo].[i_qfii_other_flows]
    where ticker = 'KPCPNTFR Index' and CAST(t_date as date) >= cast(dateadd(day,{latest["KPCPNTFR Index"][1]},getdate()) as date) --T-1
    or ticker = 'INBTFINT Index' and CAST(t_date as date) >= cast(dateadd(day,{latest["INBTFINT Index"][1]},getdate()) as date) --T-1
    or ticker = 'JTBTFRN Index' and CAST(t_date as date) >= cast(dateadd(day,{latest["JTBTFRN Index"][1]},getdate()) as date)  -- (Last last Fri)
    or ticker = 'BZSIFODN Index' and CAST(t_date as date) >= cast(dateadd(day,{latest["BZSIFODN Index"][1]},getdate()) as date) -- T-3 


    select code as type ,t_date,flow = flow*power(10,6) ,cur='USD',p_no
    from  funddb.dbo.v_fof_t_data_to_countryflow_qfii
    where code = 'THIVNET$ Index'and CAST(t_date as date) >=cast(dateadd(day,{latest["THIVNET$ Index"][1]},getdate()) as date)
    or code ='VNDXNET$ Index' and CAST(t_date as date) >=cast(dateadd(day,{latest["VNDXNET$ Index"][1]},getdate()) as date)
    or code ='MATPENET Index' and CAST(t_date as date) >=cast(dateadd(day,{latest["MATPENET$ Index"][1]},getdate()) as date)"""

if __name__ == "__main__":
    db_conn = SQLModule.get_db()
    cursor = db_conn.cursor()
    current_info = get_latest_data_dates(cursor, -30)
    get_newest_sql(current_info)


# Example usage:
# connection = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_user;PWD=your_password')
# dates = get_latest_data_dates(connection)
# print(dates)

