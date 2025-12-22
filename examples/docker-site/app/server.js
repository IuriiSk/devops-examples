const express = require("express");
const { Pool } = require("pg");

const app = express();
app.use(express.urlencoded({ extended: true }));

const pool = new Pool({
    host: "db",
    user: "postgres",
    password: "password",
    database: "mydb",
    port: 5432
});

// функция ожидания базы
async function waitForDB() {
    while (true) {
        try {
            await pool.query("SELECT 1");
            console.log("Database connected");
            break;
        } catch (err) {
            console.log("Waiting for database...");
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }
}

async function start() {

    await waitForDB();

    await pool.query(`
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL
        );
    `);

    app.get("/", async (req, res) => {
        const result = await pool.query(
            "SELECT * FROM tasks ORDER BY id"
        );

        let html = `
        <h1>Мои задачи</h1>

        <form method="POST" action="/add">
            <input name="title" required>
            <button>Добавить</button>
        </form>

        <ul>
        `;

        result.rows.forEach(task => {
            html += `<li>${task.title}</li>`;
        });

        html += "</ul>";

        res.send(html);
    });

    app.post("/add", async (req, res) => {
        await pool.query(
            "INSERT INTO tasks(title) VALUES($1)",
            [req.body.title]
        );

        res.redirect("/");
    });

  app.listen(3000, "0.0.0.0", () => {

    console.log("App started on port 3000");

});
}

start();