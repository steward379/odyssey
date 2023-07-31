const signOut = (req, res) => {
  req.session.signedIn = false;
  req.session.username = null;
  req.session.signOutMessage = "Sign out successful";
  res.redirect("/");
};

module.exports = {
  signOut,
};
