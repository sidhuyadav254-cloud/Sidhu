from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

DB = 'aura.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Create tables if not exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS state (
            id INTEGER PRIMARY KEY,
            blockedApps TEXT,
            blockedWebsites TEXT,
            blockedKeywords TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS childRequests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msg TEXT,
            timestamp TEXT
        )
    ''')
    # Ensure one row exists in state
    c.execute('SELECT COUNT(*) FROM state')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO state (blockedApps, blockedWebsites, blockedKeywords) VALUES (?,?,?)',
                  ('[]','[]','[]'))
    conn.commit()
    conn.close()

# Helper functions
def get_state_from_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT blockedApps, blockedWebsites, blockedKeywords FROM state WHERE id=1')
    row = c.fetchone()
    conn.close()
    import json
    return {
        'blockedApps': json.loads(row[0]),
        'blockedWebsites': json.loads(row[1]),
        'blockedKeywords': json.loads(row[2]),
        'childRequests': get_requests_from_db()
    }

def save_state_to_db(state):
    import json
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        UPDATE state SET blockedApps=?, blockedWebsites=?, blockedKeywords=? WHERE id=1
    ''', (json.dumps(state.get('blockedApps',[])),
          json.dumps(state.get('blockedWebsites',[])),
          json.dumps(state.get('blockedKeywords',[]))
         ))
    conn.commit()
    conn.close()

def get_requests_from_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT msg, timestamp FROM childRequests ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [{'msg': r[0], 'when': r[1]} for r in rows]

def add_request_to_db(msg):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    ts = datetime.datetime.now().isoformat()
    c.execute('INSERT INTO childRequests (msg, timestamp) VALUES (?,?)', (msg, ts))
    conn.commit()
    conn.close()

# Routes
@app.route('/api/get_state', methods=['GET'])
def get_state():
    return jsonify(get_state_from_db())

@app.route('/api/save_state', methods=['POST'])
def save_state():
    data = request.json
    save_state_to_db(data)
    return jsonify({'status':'ok'})

@app.route('/api/add_request', methods=['POST'])
def add_request():
    data = request.json
    msg = data.get('msg')
    if msg:
        add_request_to_db(msg)
        return jsonify({'status':'ok'})
    return jsonify({'status':'error','msg':'No message'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
