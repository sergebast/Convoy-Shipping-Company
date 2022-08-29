import sqlite3 as sql
from message import pm
import file_processing as fp
import db_processing as dbp

file = input('Input file name\n')
f_name = fp.file_name(file)

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

    create_table_query = '''
        CREATE TABLE convoy(
        'vehicle_id' INTEGER PRIMARY KEY,
        'engine_capacity' INTEGER NOT NULL,
        'fuel_consumption' INTEGER NOT NULL,
        'maximum_load' INTEGER NOT NULL
        );
        '''

    cur.execute(create_table_query)

    data, number_rows = dbp.for_database(f_name)
    cur.executemany('INSERT INTO convoy VALUES(?, ?, ?, ?)', data)
    conn.commit()
    pm('db', number_rows, f_name)

    cur.close()

except sql.Error as error:
    print("DB ERROR!!!", error)
finally:
    if conn:
        conn.close()
