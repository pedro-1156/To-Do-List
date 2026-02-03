import psycopg2
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
def connect_db():
    conn = psycopg2.connect(
        host="yourhost",
        database="dbname",
        user="yourusername",
        password="yourpassword"
    )
    return conn

conn = connect_db()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tarefas (
                      id SERIAL PRIMARY KEY,
                      titulo TEXT NOT NULL,
                      feito BOOL NOT NULL DEFAULT FALSE
                  )
    """)
conn.commit()
cursor.close()
conn.close()
@app.route('/')
def index():
    return redirect('/tarefas')
@app.route("/tarefas", methods=["GET", "POST"])
def tarefas():
    if request.method == "GET":
        # Tarefas aperecendo na tela
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarefas ORDER BY id")
        tarefas = cursor.fetchall()
        return render_template('tarefas.html', tarefas=tarefas)
    elif request.method == "POST":
        # Botao
        conn = connect_db()
        cursor = conn.cursor()
        titulo = request.form["titulo"]
        cursor.execute("INSERT INTO tarefas (titulo, feito) VALUES (%s, %s)", (titulo, False))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/tarefas')

@app.route('/tarefas/<int:id>/feito')
def feito(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET feito = TRUE WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/tarefas')

if __name__ == '__main__':

    app.run(debug=True)
