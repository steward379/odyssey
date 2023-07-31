const express = require("express");
const router = express.Router();
const signoutController = require("../controllers/signoutController");

router.get("/", signoutController.signOut);

module.exports = router;
