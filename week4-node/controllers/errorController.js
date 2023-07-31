// controllers/errorController.js

// const imageMap = {
//   0: "/images/--00.png",
//   1: "/images/--01.png",
//   2: "/images/--02.png",
//   3: "/images/--03.png",
//   4: "/images/--04.png",
//   5: "/images/--05.png",
//   6: "/images/--06.png",
//   7: "/images/--07.png",
//   8: "/images/--08.png",
//   9: "/images/--09.png",
// };
const imageMap = require("../models/imageModel");

module.exports = {
  getErrorPage: (req, res) => {
    let message = req.query.message;
    let messages = [];
    let words = message.split(" ");

    for (let word of words) {
      let charArray = Array.from(word);
      let newMessage = "";
      let imageMessages = [];

      for (let char of charArray) {
        if (!isNaN(parseInt(char))) {
          imageMessages.push({ type: "img", content: imageMap[char] });
          if (newMessage) {
            messages.push({ type: "text", content: newMessage });
            newMessage = "";
          }
        } else {
          newMessage += char;
        }
      }
      if (newMessage) {
        messages.push({ type: "text", content: newMessage });
      }
      if (imageMessages.length) {
        messages = messages.concat(imageMessages);
      }
      if (word !== words[words.length - 1]) {
        messages.push({ type: "text", content: " " });
      }
    }

    res.render("error", {
      message: message,
      messages: messages,
    });
  },
};
