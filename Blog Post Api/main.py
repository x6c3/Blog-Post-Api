from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel
import mysql.connector
from datetime import date, datetime

app = FastAPI()
conn = mysql.connector.connect(host='localhost', user='root', password='', db='my-db')
cursor = conn.cursor()

class Posts(BaseModel):
    name: str
    timestamp: date
    post: str

@app.get('/x86/api/home')
def home():
    return {'Message': 'Hello world'}

@app.get('/x86/api/viewall')
def get_all_posts():
    sql = 'SELECT * FROM POSTS'
    cursor.execute(sql)
    posts = cursor.fetchall()

    if posts is not None:
        return json.dumps({'Blogs': posts})
    else:
        return json.dumps({'Error': 'No Posts Found'})

@app.post('/x86/api/createpost')
def create_post(posts: Posts):
    sql = 'INSERT INTO posts VALUES (%s, %s, %s)'
    values = (posts.name, posts.timestamp.isoformat(), posts.post)

    try:
        cursor.execute(sql, values)
        conn.commit()
        return json.dumps({'Message': 'Successfully created your post'})
    except Exception as e:
        return json.dumps({'Error': f'Something went wrong {str(e)}'})
