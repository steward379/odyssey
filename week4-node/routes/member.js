const express = require("express");
const router = express.Router();
const memberController = require("../controllers/memberController");

router.get("/:username", memberController.getMember);

module.exports = router;
