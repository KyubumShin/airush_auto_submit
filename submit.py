import re
import sqlite3
import subprocess
import time
from datetime import datetime
from multiprocessing import Process

import pandas as pd
import argparse

nsml_name = "KR96342"  # NSML ID 넣는 곳
data_name = "airush2022-1-3"  # 데이터 셋
submit_list_path = './submit.csv'
S_HOUR = 3601


def insert_data(session, model, score):
    model = model if isinstance(model, str) else str(model)
    session = session if isinstance(session, str) else str(session)
    conn = sqlite3.connect("submit.db")
    cur = conn.cursor()
    cur.execute('INSERT INTO submit_data VALUES (?, ?, ?, ?)',
                (f'{session}/{model}', session, model, score))
    conn.commit()
    conn.close()


def run_submit(command, session, model):
    now = time.time()
    print(f"[Command] {command}")
    print(datetime.now())
    complete_process = subprocess.run(command, capture_output=True)
    print(complete_process.stdout.decode('utf-8'))
    try:
        score = complete_process.stdout.decode('utf-8').split('Score:')[-1]
        score = re.sub(r"[^\d.]", '', score)
        score = float(score)
    except:
        print("Submit Fail")
        return 0

    insert_data(session, model, score)

    print(f"[Collapsed time] {time.time() - now}")


def check_db():
    conn = sqlite3.connect('submit.db')
    cur = conn.cursor()
    try:
        cur.execute(''' SELECT count(id) FROM submit_data''')
    except:
        conn.execute("CREATE TABLE submit_data(id TEXT, session TEXT, checkpoint TEXT, score REAL)")
    finally:
        print("DB Check Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-wt", type=int, default=0)
    parser.add_argument("-e", type=str, default=None)
    args = parser.parse_args()

    li_procs = []
    s_df = pd.read_csv(submit_list_path)
    check_db()
    for i in range(s_df.shape[0]):
        s = s_df.session[i]
        m = s_df.model[i]
        full_session = '/'.join([nsml_name, data_name, str(s)])
        if not args.e:
            full_command = f"nsml submit {full_session} {m} --esm {nsml_name}"
        else:
            full_command = f"nsml submit {full_session} {m} --esm {nsml_name} -e {args.e}"
        li_procs.append(Process(target=run_submit, args=(full_command, s, m)))

    now = time.time()
    time.sleep(args.wt)

    for i, proc in enumerate(li_procs):
        proc.start()
        if i + 1 < len(li_procs):
            time.sleep(S_HOUR)

    for proc in li_procs:
        proc.join()
    print(f"Total collapsed time: {time.time() - now}")
