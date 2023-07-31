// controllers/squaredController.js

const imageMap = require("../models/imageModel");

const calculateSquared = (req, res) => {
  const integerInput = req.params.integer;

  if (!/^[1-9]\d*$/.test(integerInput)) {
    res.redirect("/error?message=" + encodeURIComponent("4 - Invalid integer"));
    return;
  }
  const integer = parseInt(integerInput, 10);
  const squared = integer * integer;
  const digits = String(squared).split("").map(Number);

  if (!digits.every((digit) => digit in imageMap)) {
    res.redirect(
      "/error?message=" +
        encodeURIComponent("5 - Invalid digit in squared number")
    );
    return;
  }
  const imageUrls = digits.map((digit) => imageMap[digit]);
  res.render("square", { integer, squared, image_urls: imageUrls });
};

module.exports = {
  calculateSquared,
};
