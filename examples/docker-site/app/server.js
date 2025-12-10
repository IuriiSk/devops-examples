const express = require("express");
const { Pool } = require("pg");

const app = express();
app.use(express.urlencoded({ extended: true }));

const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: 5432,
});

// тестовый роут
app.get("/", async (req, res) => {
  try {
    const result = await pool.query("SELECT NOW()");
    res.send(`DB connected: ${result.rows[0].now}`);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

app.listen(3000, () => {
  console.log("App running on port 3000");
});