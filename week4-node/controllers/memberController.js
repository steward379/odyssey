// controllers/memberController.js

const userModel = require("../models/userModel");

const getMember = (req, res) => {
  console.log("User route called");

  const { username } = req.params;

  if (req.session.signedIn) {
    // const query = "SELECT image_url FROM users WHERE username = $1";
    // const values = [username];
    // pool.query(query, values, (err, result) => {

    userModel.getUserImageByUsername(username, (err, result) => {
      if (err) {
        console.error(err);
        res.redirect("/error?message=" + encodeURIComponent("8" + err.message));
      } else {
        const userImage = result.rows[0] ? result.rows[0].image_url : null;
        const userImageMap = { [username]: userImage };
        res.render("member", {
          username,
          user_image_map: userImageMap,
          user_image: userImage,
        });
      }
    });
  } else {
    res.redirect(
      "/error?message=" + encodeURIComponent("3 - Please sign in first")
    );
  }
};

module.exports = {
  getMember,
};
