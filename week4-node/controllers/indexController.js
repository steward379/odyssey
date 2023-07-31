module.exports = {
  getHomePage: (req, res) => {
    let signOutMessage = null;

    if (req.session.signOutMessage) {
      signOutMessage = req.session.signOutMessage;
      req.session.signOutMessage = null; // clear the message after using it
    }

    res.render("index", {
      username: req.session.username,
      integer: req.session.integer,
      signOutMessage: signOutMessage,
    });
  },
};
