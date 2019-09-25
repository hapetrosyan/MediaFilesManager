import pyodbc
import pandas as pd

class mssql:

    server = 'localhost'
    database = 'HandlePhotos'

    if env == 'local':
        cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=localhost;"
                              "Database=AdventureWorksDW2012;"
                              "Trusted_Connection=yes;")
    elif env == 'prod':
        cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=corp-bi;"
                              "Database=ReportingDW;"
                              "Trusted_Connection=yes;")
    else:
        print('provide correct environment')
        exit()

    def run_sp(sp_name, params):

        params = ["'" + str(param) + "'" for param in params]
        params_string = ",".join(params)
        cursor = cnxn.cursor()
        cursor.execute('EXEC ' + sp_name + " " + params_string)

        print('EXEC ' + sp_name + " " + params_string)

        if cursor.description is None:
            print('cursor is none')
            cursor.commit()
            return (['SP executed'])

        else:
            multiple_rows = [dict(list(zip(list(zip(*cursor.description))[0], row))) for row in cursor.fetchall()]
            return pd.DataFrame(data = multiple_rows)