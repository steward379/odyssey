$(document).ready(function () {
  $("#loadingDiv").hide();
});

$(window).on("beforeunload", function () {
  $("#loadingDiv").show();
});

function validateForm(fields) {
  for (const field of fields) {
    if (
      isFieldEmpty(field.value) ||
      (field.type === "checkbox" && !field.checked)
    ) {
      alert(
        `${
          field.name.charAt(0).toUpperCase() + field.name.slice(1)
        } cannot be empty`
      );
      return false;
    }
  }
  return true;
}

function validateSignUpForm() {
  const form = document.forms["signupForm"];

  return validateForm([
    form["name"],
    form["username"],
    form["password"],
    form["checkbox"],
  ]);
}

function validateSignInForm() {
  const form = document.forms["signInForm"];
  return validateForm([form["username"], form["password"], form["checkbox"]]);
}

function isFieldEmpty(value) {
  return !value || value.trim() === "";
}

function validateCommentForm() {
  const comment = document.forms["commentForm"]["content"].value;

  if (isFieldEmpty(comment)) {
    alert("Comment cannot be empty");
    return false;
  }
}

function confirmDelete(commentId) {
  if (confirm("確定要刪除這條留言嗎？")) {
    let form = document.createElement("form");
    form.method = "POST";
    form.action = "/deleteMessage";

    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "comment_id";
    input.value = commentId;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
  }
}

if (window.location.pathname === "/") {
  window.onload = function () {
    const forms = [".sign-in-form", ".square-form"];

    forms.forEach((formSelector) => {
      const form = document.querySelector(formSelector);

      form.addEventListener("mouseover", function () {
        form.classList.add("hovered");
        forms
          .filter((selector) => selector !== formSelector)
          .forEach((otherFormSelector) => {
            document
              .querySelector(otherFormSelector)
              .classList.add("unhovered");
          });
      });

      form.addEventListener("mouseout", function () {
        form.classList.remove("hovered");
        forms
          .filter((selector) => selector !== formSelector)
          .forEach((otherFormSelector) => {
            document
              .querySelector(otherFormSelector)
              .classList.remove("unhovered");
          });
      });
    });
  };
}

// window.onload = function () {
//   const signInForm = document.querySelector(".sign-in-form");
//   const squareForm = document.querySelector(".square-form");

//   console.log(signInForm);
//   console.log(squareForm);

//   signInForm.addEventListener("mouseover", function () {
//     signInForm.classList.add("hovered");
//     squareForm.classList.add("unhovered");
//   });
//   signInForm.addEventListener("mouseout", function () {
//     signInForm.classList.remove("hovered");
//     squareForm.classList.remove("unhovered");
//   });
//   squareForm.addEventListener("mouseover", function () {
//     squareForm.classList.add("hovered");
//     signInForm.classList.add("unhovered");
//   });
//   squareForm.addEventListener("mouseout", function () {
//     squareForm.classList.remove("hovered");
//     signInForm.classList.remove("unhovered");
//   });
// };

function searchMember() {
  const username = document.getElementById("username_search").value;

  web_domain = "http://127.0.0.1:3000/";

  fetch(`${web_domain}api/member?username=${username}`, {
    method: "GET",
  })
    // .then((res) => res.text())
    // .then((text) => {
    //   console.log("Raw response text:", text);
    //   try {
    //     return JSON.parse(text);
    //   } catch (error) {
    //     throw new Error("Failed to parse response as JSON");
    //   }
    // })
    .then((res) => res.json())
    .then((data) => {
      console.log(data.data);

      const memberInfoDiv = document.getElementById("memberInfo");

      // if (data && data.data && data.data.username) {
      if (data?.data?.username) {
        console.log(data.username);
        memberInfoDiv.innerHTML = `
              <p>${data.data.name} (${data.data.username})</p>
          `;
      } else {
        memberInfoDiv.innerHTML = "<p><i>找不到此會員資料</i></p>";
      }
    })
    .catch((err) => {
      console.error("Error:", err);
    });
}

function updateName() {
  const newName = document.getElementById("newName").value;

  fetch("/api/member", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: newName,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.ok) {
        document.getElementById("updateStatus").innerText = "更新成功 🎉";
      } else {
        document.getElementById("updateStatus").innerText = "更新失敗 😠";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("updateStatus").innerText = "出錯了！";
    });
}

// deprecated

// function validateNumber() {
//   const square = document.getElementById("square");

//   const squareNum = square.value;

//   if (!/^\d+$/.test(squareNum) || parseInt(squareNum) <= 0) {
//     alert("Please enter a positive number");
//     return false;
//   }
//   window.location.href = "/squared/" + squareNum;
//   return false;
// }
