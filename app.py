from flask import Flask
import psycopg2
Host = "ec2-52-20-166-21.compute-1.amazonaws.com"
Database = "d6re5m4gmvtalp"
User = "ybeylittvmuyzj"
Port= 5432
Password = "75d7775c33b597e7a3269903dfbfc8f1a79018f6c252581d9ad3768991cffb1d"

app = Flask(__name__)

conn = psycopg2.connect(dbname = Database, user = User ,password = Password, host = Host)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
conn.close()