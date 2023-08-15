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

function validateNumber() {
  const square = document.getElementById("square");
  const squareNum = square.value;

  if (!/^\d+$/.test(squareNum) || parseInt(squareNum) <= 0) {
    alert("Please enter a positive number");
    return false;
  }

  window.location.href = "/squared/" + squareNum;
  return false;
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

window.onload = function () {
  const forms = [".sign-in-form", ".square-form"];

  forms.forEach((formSelector) => {
    const form = document.querySelector(formSelector);

    form.addEventListener("mouseover", function () {
      form.classList.add("hovered");
      forms
        .filter((selector) => selector !== formSelector)
        .forEach((otherFormSelector) => {
          document.querySelector(otherFormSelector).classList.add("unhovered");
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

$(document).ready(function () {
  $("#loadingDiv").hide();
});

$(window).on("beforeunload", function () {
  $("#loadingDiv").show();
});

function validateNumber() {
  const square = document.getElementById("square");

  const squareNum = square.value;

  if (!/^\d+$/.test(squareNum) || parseInt(squareNum) <= 0) {
    alert("Please enter a positive number");
    return false;
  }
  window.location.href = "/squared/" + squareNum;
  return false;
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

window.onload = function () {
  const signInForm = document.querySelector(".sign-in-form");
  const squareForm = document.querySelector(".square-form");

  console.log(signInForm);
  console.log(squareForm);

  signInForm.addEventListener("mouseover", function () {
    signInForm.classList.add("hovered");
    squareForm.classList.add("unhovered");
  });
  signInForm.addEventListener("mouseout", function () {
    signInForm.classList.remove("hovered");
    squareForm.classList.remove("unhovered");
  });
  squareForm.addEventListener("mouseover", function () {
    squareForm.classList.add("hovered");
    signInForm.classList.add("unhovered");
  });
  squareForm.addEventListener("mouseout", function () {
    squareForm.classList.remove("hovered");
    signInForm.classList.remove("unhovered");
  });
};

$(document).ready(function () {
  $("#loadingDiv").hide();
});

$(window).on("beforeunload", function () {
  $("#loadingDiv").show();
});
