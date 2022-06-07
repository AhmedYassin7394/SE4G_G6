from flask import Flask, render_template, request, redirect, url_for, session, flash, g

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from psycopg2 import connect


#This function creates a connection to the database saved in Database.txt

def conn_db():
    if 'db' not in g:
        
        g.db =  connect("dbname=waste user=postgres password=ALJANA")
    
    return g.db

def enddb_conn():
    if 'db' in g:
        g.db.close()
        g.pop('db')
        
# Create the application instance
app = Flask(__name__, template_folder="templates")
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/Register', methods=('POST', 'GET'))
@app.route('/register', methods=('POST', 'GET'))
def register():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        adress   = request.form['adress']
        error    = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not adress: 
            error = 'adress required.'
        else :
            conn = conn_db()
            cur = conn.cursor()
            cur.execute(
            'SELECT userid FROM system_table WHERE username = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already exist!!.'.format(username)
                cur.close()
                conn.close()

        if error is None:
            cur.execute(
                'INSERT INTO system_table (username, password, adress) VALUES (%s, %s, %s)',
                (username, generate_password_hash(password), adress)
            )
            cur.close()
            conn.commit()
            conn.close()
            return redirect(url_for('LOGIN'))

        flash(error)

     return render_template('register.html')

@app.route('/LOGIN', methods=('POST', 'GET'))
@app.route('/LOGIN', methods=('POST', 'GET'))
def LOGIN():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        conn = conn_db()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM system_table WHERE username = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()

        if user is None:
            error = 'Login failed wrong username.'
        elif not check_password_hash(user[2], password):
            error = 'Login failed wrong password.'

        if error is None:
            session.clear()
            session['userid'] = user[0]
            return redirect(url_for('HOME'))

        flash(error)

    return render_template('LOGIN.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('HOME'))

#@app.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = conn_db()
        cur = conn.cursor()
        cur.execute(
                    'SELECT * FROM system_table WHERE user_id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()
    if g.user is None:
        return False
    else: 
        return True


# Create a URL route in our application for "/"
@app.route('/')
@app.route('/HOME')
def     HOME():
    conn = conn_db()
    cur = conn.cursor()
    cur.execute(
             """SELECT system_table.username, post.post_id, post.created, post.title, post.body 
                FROM system_table, post WHERE  
                     system_table.userid = post.author_id"""
                    )
    posts = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    load_logged_in_user()

    return render_template('HOME.html', posts=posts)

@app.route('/Map')
def Map():
     return render_template('Map.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
 app.run(debug=True)