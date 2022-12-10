Host = "biuwbczwo7b578wwfjsu-postgresql.services.clever-cloud.com"
Database = "biuwbczwo7b578wwfjsu"
User = "uxv0hxett3sicwdz1pue"
Port= 5432
Password = "5FbcFUac59mo5FC5AR7N"

from datetime import date
from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS, cross_origin
import secrets
import string
import datetime


app = Flask(__name__)
CORS(app)
# conn = psycopg2.connect(dbname = Database, user = User ,password = Password, host = Host)
# cur = conn.cursor()
# cur.execute("CREATE TABLE uv_data(uv_id VARCHAR(6) PRIMARY KEY,date DATE,accused VARCHAR(150), des_sm VARCHAR(200), des_lg VARCHAR(1000), severity INT DEFAULT 1, upvotes INT DEFAULT 0 , downvotes INT DEFAULT 0)")
# cur.execute("INSERT INTO uv_data VALUES('asdere','03-11-2022','ahshdjdns','desc small','desc_long','2','1','3')")
# cur.execute("SELECT * FROM uv_data")
# x = cur.fetchall()
# print(x)
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
    

@app.route('/count',methods=["POST"])
def count():
    conn = connectDB()
    cur = conn.cursor()
    getCountQuery = "SELECT COUNT(*) FROM uv_data"
    cur.execute(getCountQuery)
    count =  cur.fetchone()[0]
    # print(count)
    # cur.execute("SELECT * FROM uv_data")
    # x = cur.fetchall()
    # print(x)
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
    severity = uvData[0]['severity']
    differnce = int(uvData[0]['upvotes']) - int(uvData[0]['downvotes'])
    if differnce > 0 :
        severity = 3
    elif differnce <0:
        severity = 1
    else :
        severity = 2
    updateSeverityQuery = "UPDATE uv_data SET severity = %s WHERE uv_id = %s"
    cur.execute(updateSeverityQuery,(severity,uvId))
    conn.commit()
    uvData[0]['severity'] = severity
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

@app.route('/upvote',methods=['POST'])
def upvote():
    conn = connectDB()
    cur = conn.cursor()
    uvId = request.get_json()['uvId']
    updateUpvoteQuery = "UPDATE uv_data SET upvotes= upvotes+1 WHERE uv_id = %s"
    cur.execute(updateUpvoteQuery,(uvId,))
    conn.commit()
    conn.close()
    return "success", 200

@app.route('/downvote',methods=['POST'])
def downvote():
    conn = connectDB()
    cur = conn.cursor()
    uvId = request.get_json()['uvId']
    updateDownvoteQuery = "UPDATE uv_data SET downvotes = downvotes+1 WHERE uv_id = %s"
    cur.execute(updateDownvoteQuery,(uvId,))
    conn.commit()
    conn.close()
    return "success", 200