import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import express from "express";
import cors from "cors";
import { ApolloServer } from "@apollo/server";
import { expressMiddleware } from "@apollo/server/express4";
import { GraphQLError } from "graphql";
import { pool } from "./db.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const typeDefs = fs.readFileSync(path.join(__dirname, "schema.graphql"), "utf8");

// MySQL row -> GraphQL Dish
const toDish = (r) => ({
  id: r.id,
  name: r.name,
  price: r.price,
  available: Boolean(r.available),
  description: r.description,
});

const resolvers = {
  Query: {
    // list: optional WHERE available = 1
    dishes: async (_, { availableOnly }) => {
      const sql = availableOnly
        ? "SELECT * FROM dishes WHERE available = 1 ORDER BY id"
        : "SELECT * FROM dishes ORDER BY id";
      const [rows] = await pool.query(sql);
      return rows.map(toDish);
    },
    // by-id: WHERE id = ?
    dish: async (_, { id }) => {
      const [rows] = await pool.query("SELECT * FROM dishes WHERE id = ?", [id]);
      return rows.length ? toDish(rows[0]) : null;
    },
  },
  Mutation: {
    // INSERT
    addDish: async (_, { input }) => {
      const name = input.name.trim();
      if (!name) throw new GraphQLError("name must not be empty", { extensions: { code: "BAD_USER_INPUT" } });
      if (input.price < 0) throw new GraphQLError("price must be >= 0", { extensions: { code: "BAD_USER_INPUT" } });
      const [res] = await pool.query(
        "INSERT INTO dishes (name, price, available, description) VALUES (?, ?, ?, ?)",
        [name, input.price, input.available ?? true, input.description ?? null]
      );
      const [rows] = await pool.query("SELECT * FROM dishes WHERE id = ?", [res.insertId]);
      return toDish(rows[0]);
    },
    // UPDATE
    setDishAvailability: async (_, { id, available }) => {
      await pool.query("UPDATE dishes SET available = ? WHERE id = ?", [available, id]);
      const [rows] = await pool.query("SELECT * FROM dishes WHERE id = ?", [id]);
      return rows.length ? toDish(rows[0]) : null;
    },
  },
};

const app = express();
const server = new ApolloServer({ typeDefs, resolvers });
await server.start();

app.use("/graphql", cors(), express.json(), expressMiddleware(server));
app.use(express.static(path.join(__dirname, "public")));

const PORT = Number(process.env.PORT || 4000);
app.listen(PORT, () => {
  console.log(`CampusEats GraphQL ready: http://localhost:${PORT}/graphql`);
  console.log(`Front-end page:            http://localhost:${PORT}/`);
});
