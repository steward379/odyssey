const userModel = require("../models/userModel");

const postSignin = (req, res) => {
  const { username, password, consent, loveMe } = req.body;
  console.log(consent, loveMe);

  if (!username || !password) {
    res.redirect(
      "/error?message=" +
        encodeURIComponent("1 - Please provide username and password")
    );
    return;
  }

  userModel.getUserByUsername(username, (err, result) => {
    if (err) {
      res.redirect(
        "/error?message=" + encodeURIComponent("9 - " + err.message)
      );
      return;
    }
    if (result.rows.length === 0 || password !== username) {
      res.redirect(
        "/error?message=" +
          encodeURIComponent("2 - Invalid username or password")
      );
      return;
    }
    req.session.signedIn = true;
    req.session.username = username;
    req.session.userImage = result.rows[0].image_url;

    res.redirect(`/member/${username}`);
  });
};

module.exports = {
  postSignin,
};
