const express = require("express");
const router = express.Router();
const squaredController = require("../controllers/squaredController");

router.get("/:integer", squaredController.calculateSquared);

module.exports = router;
