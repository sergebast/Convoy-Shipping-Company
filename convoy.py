import sqlite3 as sql
import pandas as pd
import json
from message import pm
import file_processing as fp
import db_processing as dbp

file = input('Input file name\n')
f_name = fp.file_name(file)

if not file.endswith('.s3db'):
    if file.count('[CHECKED]') == 0:
        if file.endswith('.xlsx'):
            lines = fp.xlsx_to_csv(file, f_name)
            pm('lines', lines, f_name)

        data, cells = fp.corrected_data(f_name)
        fp.writer_csv(data, f_name)
        pm('cells', cells, f_name)

    try:
        conn = sql.connect(f'{f_name}.s3db')
        cur = conn.cursor()

        create_table_query = "CREATE TABLE IF NOT EXISTS convoy(\
            'vehicle_id' INTEGER PRIMARY KEY,\
            'engine_capacity' INTEGER NOT NULL,\
            'fuel_consumption' INTEGER NOT NULL,\
            'maximum_load' INTEGER NOT NULL\
            );"

        cur.execute(create_table_query)

        cur.execute('DELETE FROM convoy')

        cur.execute('ALTER TABLE convoy ADD COLUMN score INTEGER NOT NULL')
        conn.commit()

        data = dbp.for_database(f_name)
        cur.executemany('INSERT INTO convoy VALUES(?, ?, ?, ?, ?)', data)
        conn.commit()

        pm('db', cur.rowcount, f_name)

        cur.close()
        if conn:
            conn.close()

    except sql.Error as error:
        print("DB ERROR!!!", error)

else:
    try:
        conn = sql.connect(f'{f_name}.s3db')
        cur = conn.cursor()

        create_table_query = "CREATE TABLE IF NOT EXISTS convoy(\
                    'vehicle_id' INTEGER PRIMARY KEY,\
                    'engine_capacity' INTEGER NOT NULL,\
                    'fuel_consumption' INTEGER NOT NULL,\
                    'maximum_load' INTEGER NOT NULL,\
                    'score' INTEGER NOT NULL);"

        cur.execute(create_table_query)
        cur.close()
        if conn:
            conn.close()
    except sql.Error as error:
        print("DB ERROR!!!", error)

try:
    conn = sql.connect(f'{f_name}.s3db')
    df_json = pd.read_sql_query(
        'SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load FROM convoy WHERE score > 3', conn)
    df_json.reset_index(drop=True, inplace=True)
    with open(f'{f_name}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict(convoy=json.loads(df_json.to_json(orient='records')))))

    df_xml = pd.read_sql_query(
        'SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load FROM convoy WHERE score <= 3', conn)
    with open(f'{f_name}.xml', 'w', encoding='utf-8') as f:
        if len(df_xml) == 0:
            f.write('<convoy></convoy>')
        else:
            f.write(df_xml.to_xml(index=False, root_name='convoy', row_name='vehicle', xml_declaration=False))

    pm('json', len(df_json), f_name)
    pm('xml', len(df_xml), f_name)
except sql.Error as error:
    print("DB ERROR!!!", error)
