import sqlite3
import subprocess
import time

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

user_id = "KR96342"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
conn = sqlite3.connect('submit.db')
conn.row_factory = sqlite3.Row


def db_check():
    cur = conn.cursor()
    try:
        cur.execute(''' SELECT count(id) FROM submit_data''')
    except:
        conn.execute("CREATE TABLE submit_data(id TEXT, session TEXT, checkpoint TEXT, score REAL, cv REAL)")
    try:
        cur.execute(''' SELECT count(session) FROM session_data''')
    except:
        conn.execute("CREATE TABLE session_data(session TEXT, model Text, dataset Text,description Text)")
    finally:
        print("DB Check Done")


db_check()


@app.get('/')
async def index(request: Request):
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM session_data CROSS JOIN submit_data sd on session_data.session = sd.session ORDER BY score
    """)
    rows = cur.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, 'sessions': rows})


@app.get('/session/{session}')
async def session(request: Request, session):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM submit_data WHERE session=? ORDER BY score
        """, (session,))
    rows = cur.fetchall()
    return templates.TemplateResponse("session.html", {"request": request, 'sessions': rows})


def nsml_memo(dataset, session_id, model, desc):
    time.sleep(1)
    full_commands = f'nsml memo {user_id}/{dataset}/{session_id} "model : {model}, desc: {desc}"'
    subprocess.run(full_commands)


@app.post('/memo', response_class=RedirectResponse, status_code=302)
async def memo(background_task: BackgroundTasks, dataset: str = Form(), session_id: str = Form(), model: str = Form(),
               desc: str = Form()):
    cur = conn.cursor()
    cur.execute("SELECT * FROM session_data WHERE session=?", (session_id,))
    rows = cur.fetchall()
    if rows:
        cur.execute("UPDATE session_data SET description=? ,model=?, dataset=? WHERE session=?",
                    (desc, model, dataset, session_id))
    else:
        cur.execute('INSERT INTO session_data VALUES (?, ?, ?, ?)', (session_id, model, dataset, desc))
    conn.commit()
    background_task.add_task(nsml_memo, dataset=dataset, session_id=session_id, desc=desc, model=model)
    return '/'


@app.post('/submit')
async def submit(background_task: BackgroundTasks, dataset: str = Form(), session_id: str = Form(),
                 checkpoint: str = Form(),
                 desc: str = Form()):
    pass
