import mysql from "mysql2/promise";

// Override with environment variables if your MySQL setup differs.
export const pool = mysql.createPool({
  host: process.env.DB_HOST || "localhost",
  port: Number(process.env.DB_PORT || 3306),
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD || "",
  database: process.env.DB_NAME || "campuseats_catalogue",
  decimalNumbers: true, // return DECIMAL as JS numbers (GraphQL Float)
  waitForConnections: true,
  connectionLimit: 5,
});
