from flask import Flask, render_template, request, redirect
import psycopg2
import os
import time

app = Flask(__name__)

# ✅ ВАЖНО: имя сервиса в docker-compose = db
DB_HOST = os.environ.get("POSTGRES_HOST", "db")
DB_NAME = os.environ.get("POSTGRES_DB", "postgres")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "12345")


def get_db_connection():
    """Подключение к БД с retry"""
    for i in range(15):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            print(f"⏳ DB not ready... retry {i+1}/15")
            time.sleep(2)

    raise Exception("❌ Could not connect to DB")


def init_db():
    """Создание таблицы"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ DB initialized")


# ⚠️ теперь безопаснее
print("⏳ Waiting DB before init...")
init_db()


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, completed FROM todos ORDER BY id DESC;")
    todos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO todos (title) VALUES (%s);", (title,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM todos WHERE id = %s;", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')


@app.route('/health')
def health():
    return {"status": "ok"}


if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)