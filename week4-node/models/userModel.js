const pool = require("./db");

const getUserByUsername = (username, callback) => {
  pool.query("SELECT * FROM users WHERE username = $1", [username], callback);
};

const getUserImageByUsername = (username, callback) => {
  pool.query(
    "SELECT image_url FROM users WHERE username = $1",
    [username],
    callback
  );
};

module.exports = {
  getUserByUsername,
  getUserImageByUsername,
};
