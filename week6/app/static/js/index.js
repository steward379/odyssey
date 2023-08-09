function validateSignUpForm() {
  const name = document.forms["signupForm"]["name"].value;
  const username = document.forms["signupForm"]["username"].value;
  const password = document.forms["signupForm"]["password"].value;
  const checkbox = document.forms["signupForm"]["checkbox"].checked;

  if (name == "" || username == "" || password == "" || !checkbox) {
    alert("All fields must be filled out");
    return false;
  }
}

function validateSignInForm() {
  const username = document.forms["signInForm"]["username"].value;
  const password = document.forms["signInForm"]["password"].value;
  const checkbox = document.forms["signInForm"]["checkbox"].checked;

  if (username == "" || password == "" || !checkbox) {
    alert("All fields must be filled out");
    return false;
  }
}

function validateCommentForm() {
  const comment = document.forms["commentForm"]["content"].value;

  console.log(comment);

  if (comment.trim() == "") {
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
