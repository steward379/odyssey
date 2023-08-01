const express = require("express");
const session = require("express-session");
const cookieParser = require("cookie-parser");
const ejs = require("ejs");
const { parse } = require("dotenv");
const memberRoutes = require("../routes/member");
const signoutRoutes = require("../routes/signout");
const homeRoutes = require("../routes/index");
const signinRoutes = require("../routes/signin");
const squaredRoutes = require("../routes/squared");
const errorRoutes = require("../routes/error");

// const crypto = require("crypto");
// const secret = crypto.randomBytes(64).toString("hex");
// console.log(secret);

require("dotenv").config();

const app = express();
app.use(express.static("public"));

app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
  })
);

// const { Pool } = require("pg");

// const pool = new Pool({
//   user: "steward",
//   host: "localhost",
//   database: "expressdb",
//   password: "steward",
//   port: 5432,
// });

// const pool = require("./models/db.js");
// console.log(pool.query);

// pool.query("SELECT * FROM users", (error, results) => {
//   if (error) {
//     throw error;
//   }
//   console.log(results.rows);
// });

// already in db
// const validUsers = ["orc", "test", "admin"];

app.engine("ejs", ejs.__express);
app.set("view engine", "ejs");

app.use("/", homeRoutes);
app.use("/sign_in", signinRoutes);
app.use("/sign_out", signoutRoutes);

//index

// app.get("/", function (req, res) {
//   let signOutMessage = null;

//   if (req.session.signOutMessage) {
//     signOutMessage = req.session.signOutMessage;
//     req.session.signOutMessage = null; // clear the message after using it
//   }

//   res.render("index", {
//     username: req.session.username,
//     integer: req.session.integer,
//     signOutMessage: signOutMessage,
//   });
// });

//sign_in

// app.post("/sign_in", (req, res) => {
//   const { username, password, consent, loveMe } = req.body;
//   console.log(consent, loveMe);

//   if (!username || !password) {
//     res.redirect(
//       "/error?message=" +
//         encodeURIComponent("1 - Please provide username and password")
//     );
//     return;
//   }
//   // if (!validUsers.includes(username) || password !== username) {
//   //   res.redirect(
//   //     "/error?message=" + encodeURIComponent("2 - Invalid username or password")
//   //   );
//   //   return;
//   // }

//   // 在此，我們假設只要 username 是 validUsers 中的一員，就視為登入成功
//   // req.session.signedIn = true;
//   // req.session.username = username;

//   // const userImageMap = {
//   //   orc: "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/7c79cbea-6f74-4dd8-86a0-3d9870b26d9f/dd3o7up-a21bc4e7-41b9-4b73-b100-53fe549f38f3.png/v1/fill/w_1024,h_610,q_80,strp/dnd_characters_by_zetrystan_dd3o7up-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NjEwIiwicGF0aCI6IlwvZlwvN2M3OWNiZWEtNmY3NC00ZGQ4LTg2YTAtM2Q5ODcwYjI2ZDlmXC9kZDNvN3VwLWEyMWJjNGU3LTQxYjktNGI3My1iMTAwLTUzZmU1NDlmMzhmMy5wbmciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.a944xGWAwpZoUzt_7440RjUupOwoRidMfLEeErdNK1M",
//   //   admin: "/images/rick.jpeg",
//   // };
//   // req.session.userImage = userImageMap[username];

//   // res.redirect(`/member/${username}`);

//   // pool.query(
//   pool.query(
//     "SELECT * FROM users WHERE username = $1",
//     [username],
//     (err, result) => {
//       if (err) {
//         res.redirect(
//           "/error?message=" + encodeURIComponent("9 - " + err.message)
//         );
//         return;
//       }
//       if (result.rows.length === 0 || password !== username) {
//         res.redirect(
//           "/error?message=" +
//             encodeURIComponent("2 - Invalid username or password")
//         );
//         return;
//       }
//       req.session.signedIn = true;
//       req.session.username = username;
//       req.session.userImage = result.rows[0].image_url;

//       // res.redirect(`/member/${username}`);
//       res.redirect(`/member/${username}`);
//     }
//   );
// });

//sign_out

// app.get("/sign_out", (req, res) => {
//   req.session.signedIn = false;
//   req.session.username = null;
//   req.session.signOutMessage = "Sign out successful";
//   res.redirect("/");
// });

app.use("/squared", squaredRoutes);

// app.get("/squared/:integer", (req, res) => {
//   const integerInput = req.params.integer;

//   // if (isNaN(integer)) {
//   if (!/^[1-9]\d*$/.test(integerInput)) {
//     res.redirect("/error?message=" + encodeURIComponent("4 - Invalid integer"));
//     return;
//   }
//   const integer = parseInt(integerInput, 10);
//   const squared = integer * integer;
//   const digits = String(squared).split("").map(Number);

//   if (!digits.every((digit) => digit in imageMap)) {
//     res.redirect(
//       "/error?message=" +
//         encodeURIComponent("5 - Invalid digit in squared number")
//     );
//     return;
//   }
//   const imageUrls = digits.map((digit) => imageMap[digit]);
//   res.render("square", { integer, squared, image_urls: imageUrls });
// });

app.use("/member", memberRoutes);

// app.get("/member/:username", (req, res) => {
//   const { username } = req.params;

//   // if (req.session.signedIn) {
//   //   res.render("member", { username, user_image: req.session.userImageMap });
//   // } else {
//   //   res.redirect(
//   //     "/error?message=" + encodeURIComponent("3 - Please sign in first")
//   //   );
//   // }

//   if (req.session.signedIn) {
//     const query = "SELECT image_url FROM users WHERE username = $1";
//     const values = [username];
//     // pool.query(
//     pool.query(query, values, (err, result) => {
//       if (err) {
//         console.error(err);
//         res.redirect("/error?message=" + encodeURIComponent("8" + err.message));
//       } else {
//         const userImage = result.rows[0] ? result.rows[0].image_url : null;
//         const userImageMap = { [username]: userImage };
//         res.render("member", {
//           username,
//           user_image_map: userImageMap,
//           user_image: userImage,
//         });
//       }
//     });
//   } else {
//     res.redirect(
//       "/error?message=" + encodeURIComponent("3 - Please sign in first")
//     );
//   }

//   //client 作法
//   // if (req.session.signedIn) {
//   //   try {
//   //     const result = await client.query(query, values);
//   //     const userImage = result.rows[0] ? result.rows[0].image_url : null;
//   //     res.render("member", { username, user_image: userImage });
//   //   } catch (err) {
//   //     console.error(err);
//   //     res.redirect(
//   //       "/error?message=" + encodeURIComponent("8 - Database error")
//   //     );
//   //   }
//   // }
// });

app.use("/error", errorRoutes);

// app.get("/error", (req, res) => {
//   let message = req.query.message;
//   let messages = [];
//   // Split the message into words
//   let words = message.split(" ");

//   // Check each word
//   for (let word of words) {
//     let charArray = Array.from(word);
//     let newMessage = "";
//     let imageMessages = [];

//     // Check each character in the word
//     for (let char of charArray) {
//       // If the character is a digit, get the corresponding image URL and push it to imageMessages
//       if (!isNaN(parseInt(char))) {
//         imageMessages.push({ type: "img", content: imageMap[char] });
//         if (newMessage) {
//           messages.push({ type: "text", content: newMessage });
//           newMessage = "";
//         }
//       } else {
//         newMessage += char;
//       }
//     }
//     if (newMessage) {
//       messages.push({ type: "text", content: newMessage });
//     }
//     if (imageMessages.length) {
//       messages = messages.concat(imageMessages);
//     }
//     // Add a space after each word except for the last word
//     if (word !== words[words.length - 1]) {
//       messages.push({ type: "text", content: " " });
//     }
//   }

//   res.render("error", {
//     message: message,
//     messages: messages,
//   });
// });

app.use((req, res, next) => {
  const err = new Error("Not Found");
  err.status = 404;
  next(err);
});

// put it in the last of all routes
app.use((err, req, res, next) => {
  console.error(err.stack); // log the error stack trace to your server's console
  let status = err.status || 500;
  let message = encodeURIComponent(err.message);

  if (status === 404) {
    res
      .status(status)
      .redirect("/error?message=" + encodeURIComponent("404 - Not found"));
  } else {
    res.status(status).redirect("/error?message=" + "5 - " + message);
  }
});

app.listen(3000, () =>
  console.log("Server running on port 3000 at: http://localhost:3000/")
);
