from urllib.request import urlopen
import json
import psycopg2
from urls import urls1,urls2 



# database = 'sample' password = 'diva' default port 5432
conn = psycopg2.connect(database='', user='postgres',
                        password='', host='localhost', port='')

cur = conn.cursor()
bigurls = [urls1,urls2]

tablecount = 0
def create_table(ul):
    tablename = 'data'+str(tablecount)
    ls1 = []
    response = urlopen(ul)
    data_json = json.loads(response.read())
    for i in data_json.values():
        for j in i.items():
            ls1.append(j[0])

    cur.execute(f"create table if not exists {tablename}({ls1[0]} varchar(10) )")
    
    for col in range(1, len(ls1)):
        if col == 8:
            cur.execute(
                    f'alter table {tablename} add {ls1[col]} VARCHAR(255) ')
        elif col == 9:
            cur.execute(f'alter table {tablename} add {ls1[col]} JSON ')
        elif col >= 10 :
            cur.execute(f'alter table {tablename} add {ls1[col]} JSONB ')
        else:
            cur.execute(
                    f'alter table {tablename} add {ls1[col]} varchar(255) ')
    conn.commit()
    
    return f'{tablename}'
tbnames = []     
for tburl in bigurls:
    tablecount+=1 
    tbnames.append(create_table(tburl[2]))
    
print('Table created successfully....')

def bigdatafile(tbname,url):
    try:
        ls2 = []
        response = urlopen(url)
        data_json = json.loads(response.read())
        for i in data_json.values():
            for j in i.items():
                if type(j[1])==dict or type(j[1])==list:
                    ls2.append(json.dumps(j[1]))
                else:
                    ls2.append(j[1])
        
        if len(ls2)==12:
            
            cur.execute(f"insert into {tbname} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (ls2[0], ls2[1], ls2[2], ls2[3], ls2[4], ls2[5], ls2[6], ls2[7], ls2[8], ls2[9],ls2[10],ls2[11]))
            
        elif len(ls2)==13:
            
            cur.execute(f"insert into {tbname} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(ls2[0], 
            ls2[1], ls2[2], ls2[3], ls2[4], ls2[5], ls2[6], ls2[7], ls2[8], ls2[9],ls2[10],ls2[11],ls2[12]))
            
        elif len(ls2)==14:
            
            cur.execute(f"insert into {tbname} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (ls2[0], ls2[1], ls2[2], ls2[3], ls2[4], ls2[5], ls2[6], ls2[7], ls2[8], ls2[9],ls2[10],ls2[11],ls2[12],ls2[13]))

        conn.commit()
    except Exception as e:
        print('error.....',e)
        if conn:
            conn.rollback()
    
for x in tbnames:        
    for y in bigurls:
        for z in y:
            bigdatafile(x,z)
        bigurls.pop(0)
        break
    
print('Every Data Inserted Successfully.......')




    
       
