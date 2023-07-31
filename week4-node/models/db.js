const { Pool } = require("pg");
const config = require("../config/dbConfig");

const pool = new Pool(config.db);

module.exports = {
  query: (text, params, callback) => {
    console.log("Query executed, text:", text);
    console.log("Query executed, params:", params);
    return pool.query(text, params, callback);
  },
};
