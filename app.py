Host = "ec2-52-20-166-21.compute-1.amazonaws.com"
Database = "d6re5m4gmvtalp"
User = "ybeylittvmuyzj"
Port= 5432
Password = "75d7775c33b597e7a3269903dfbfc8f1a79018f6c252581d9ad3768991cffb1d"

from datetime import date
from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS, cross_origin
import secrets
import string
import datetime


app = Flask(__name__)
CORS(app)

def connectDB():
    conn = psycopg2.connect(dbname = Database, user = User ,password = Password, host = Host)
    if(conn):
        print("got connected")
    else:
        print("not connected")
    return conn

def generateID(cur):
    id = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(6)) 
    cur.execute("SELECT * FROM uv_data WHERE uv_id=%s",(id,))
    if(cur.fetchone() != None):
        id = generateID(cur)
    return id
# cur.execute("CREATE TABLE uv_data(uv_id VARCHAR(6) PRIMARY KEY,date DATE,accused VARCHAR(150), des_sm VARCHAR(200), des_lg VARCHAR(1000), severity INT DEFAULT 1, upvotes INT DEFAULT 0 , downvotes INT DEFAULT 0)")
#cur.execute("INSERT INTO uv_data VALUES('asdere','03-11-2022','ahshdjdns','desc small','desc_long','2','1','3')")
# cur.execute("SELECT * FROM uv_data")
# x = cur.fetchall()
# print(x)

@app.route('/count',methods=["POST"])
def count():
    conn = connectDB()
    cur = conn.cursor()
    getCountQuery = "SELECT COUNT(*) FROM uv_data"
    cur.execute(getCountQuery)
    count =  cur.fetchone()[0]
    print(count)
    return str(count), 200

@app.route('/',methods=["POST"])
def search():
    conn = connectDB()
    cur = conn.cursor()
    uvId = request.get_json()['uv_id']
    print(uvId)
    searchByUvIdQuery = "SELECT row_to_json(uv_data) FROM uv_data WHERE uv_id = %s"
    cur.execute(searchByUvIdQuery,(uvId,))
    uvData = cur.fetchone()
    print(uvData)
    conn.close()
    return uvData[0],200

@app.route('/add', methods=['POST'])
def add():
    conn= connectDB()
    cur = conn.cursor()
    print(request.get_json()['uvData'])
    uvData = request.get_json()['uvData']
    uvID = generateID(cur)
    dateToday = datetime.datetime.now()
    print(dateToday)
    accused = uvData['name']
    des_sm = uvData['des_sm']
    des_lg = uvData['des_lg']
    severity = uvData['severity']

    uvData = (uvID,dateToday,accused,des_sm,des_lg,severity,0,0,)
    cur.execute("INSERT INTO uv_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",uvData)
    conn.commit()
    cur.execute("SELECT * FROM uv_data")
    x = cur.fetchall()
    print(x)
    conn.close()
    return uvID,200