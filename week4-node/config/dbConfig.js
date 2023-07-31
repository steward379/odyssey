module.exports = {
  db: {
    user: process.env.DB_USER || "steward",
    host: process.env.DB_HOST || "localhost",
    database: process.env.DB_NAME || "expressdb",
    password: process.env.DB_PASSWORD || "steward",
    port: process.env.DB_PORT || 5432,
  },
};
