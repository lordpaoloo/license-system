from bottle import Bottle, run, request, response, HTTPError
import hashlib
import json
import sqlite3
"""
this is small example of license system i hope you like it and get more passion out of it
and lol man i feel sry for you if you get in backend development its sucks but its fun
and if u see it fun and cool as i see u are creep as me ,am sure u listen to radiohead and you are a fan of thom yorke

"""
app = Bottle()

def init_db():
    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            license_key TEXT PRIMARY KEY,
            user TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()
def generate_license_key(user_data):
    data = json.dumps(user_data).encode('utf-8')
    return hashlib.sha256(data).hexdigest()

@app.route('/generate', method='POST')
def generate_license():
    user_data = request.json
    if not user_data or 'user' not in user_data or 'email' not in user_data:
        raise HTTPError(400, "Invalid input. Provide 'user' and 'email' in JSON format.")

    license_key = generate_license_key(user_data)
    
    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO licenses (license_key, user, email) VALUES (?, ?, ?)', 
                   (license_key, user_data['user'], user_data['email']))
    conn.commit()
    conn.close()
    
    return {"license_key": license_key}

@app.route('/validate', method='POST')
def validate_license():
    license_key = request.json.get('license_key')
    if not license_key:
        raise HTTPError(400, "Invalid input. Provide 'license_key' in JSON format.")

    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user, email FROM licenses WHERE license_key = ?', (license_key,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"valid": True, "user": row[0], "email": row[1]}
    else:
        return {"valid": False, "message": "Invalid license key."}

if __name__ == '__main__':
    init_db()
    run(app, host='localhost', port=8080, debug=True)