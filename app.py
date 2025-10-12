from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime
import json

app = Flask(__name__)
CORS(app)

DB = 'aura.db'

# ---------- Database Initialization ----------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # State table
    c.execute('''
        CREATE TABLE IF NOT EXISTS state (
            id INTEGER PRIMARY KEY,
            blockedApps TEXT,
            blockedWebsites TEXT,
            blockedKeywords TEXT,
            screenLimit INTEGER,
            sleepFrom TEXT,
            sleepTo TEXT,
            filterLevel TEXT,
            cyberBullying INTEGER,
            predatorAlert INTEGER,
            parentPassword TEXT,
            allowChildEdit INTEGER
        )
    ''')

    # Child requests table
    c.execute('''
        CREATE TABLE IF NOT EXISTS childRequests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msg TEXT,
            timestamp TEXT
        )
    ''')

    # Insert default state if empty
    c.execute('SELECT COUNT(*) FROM state')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO state (
                blockedApps, blockedWebsites, blockedKeywords,
                screenLimit, sleepFrom, sleepTo,
                filterLevel, cyberBullying, predatorAlert,
                parentPassword, allowChildEdit
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            json.dumps(['YouTube','Instagram']),
            json.dumps(['example.com']),
            json.dumps(['violence','drugs']),
            120,
            '22:00',
            '07:00',
            'moderate',
            1,
            1,
            '1234',
            0
        ))
    conn.commit()
    conn.close()

# ---------- Helper Functions ----------
def get_state_from_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM state WHERE id=1')
    row = c.fetchone()
    conn.close()
    return {
        'blockedApps': json.loads(row[1]),
        'blockedWebsites': json.loads(row[2]),
        'blockedKeywords': json.loads(row[3]),
        'screenLimitMin': row[4],
        'sleepFrom': row[5],
        'sleepTo': row[6],
        'filterLevel': row[7],
        'cyberBullying': bool(row[8]),
        'predatorAlert': bool(row[9]),
        'parentPassword': row[10],
        'allowChildEdit': bool(row[11]),
        'childRequests': get_requests_from_db()
    }

def save_state_to_db(state):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        UPDATE state SET
        blockedApps=?, blockedWebsites=?, blockedKeywords=?,
        screenLimit=?, sleepFrom=?, sleepTo=?,
        filterLevel=?, cyberBullying=?, predatorAlert=?,
        parentPassword=?, allowChildEdit=?
        WHERE id=1
    ''', (
        json.dumps(state.get('blockedApps',[])),
        json.dumps(state.get('blockedWebsites',[])),
        json.dumps(state.get('blockedKeywords',[])),
        state.get('screenLimitMin',120),
        state.get('sleepFrom','22:00'),
        state.get('sleepTo','07:00'),
        state.get('filterLevel','moderate'),
        int(state.get('cyberBullying',True)),
        int(state.get('predatorAlert',True)),
        state.get('parentPassword','1234'),
        int(state.get('allowChildEdit',False))
    ))
    conn.commit()
    conn.close()

def get_requests_from_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT id, msg, timestamp FROM childRequests ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [{'id': r[0], 'msg': r[1], 'when': r[2]} for r in rows]

def add_request_to_db(msg):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    ts = datetime.datetime.now().isoformat()
    c.execute('INSERT INTO childRequests (msg, timestamp) VALUES (?,?)', (msg, ts))
    conn.commit()
    conn.close()

def delete_request_by_id(req_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM childRequests WHERE id=?', (req_id,))
    conn.commit()
    conn.close()

def delete_all_requests():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM childRequests')
    conn.commit()
    conn.close()

# ---------- API Endpoints ----------
@app.route('/api/get_state', methods=['GET'])
def get_state():
    return jsonify(get_state_from_db())

@app.route('/api/save_state', methods=['POST'])
def save_state_route():
    data = request.json
    save_state_to_db(data)
    return jsonify({'status':'ok'})

@app.route('/api/add_request', methods=['POST'])
def add_request_route():
    data = request.json
    msg = data.get('msg')
    if msg:
        add_request_to_db(msg)
        return jsonify({'status':'ok'})
    return jsonify({'status':'error','msg':'No message'})

@app.route('/api/approve_request', methods=['POST'])
def approve_request_route():
    data = request.json
    req_id = data.get('id')
    if req_id:
        delete_request_by_id(req_id)
        return jsonify({'status':'ok'})
    return jsonify({'status':'error','msg':'No id'})

@app.route('/api/approve_all', methods=['POST'])
def approve_all_route():
    delete_all_requests()
    return jsonify({'status':'ok'})

# ---------- Run Server ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
