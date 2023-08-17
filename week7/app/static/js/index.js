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

// comment

let userId;

function fetchUserId() {
  fetch("/api/getUserId")
    .then((res) => res.json())
    .then((data) => {
      userId = data.user_id;
      if (window.location.pathname === "/member/") {
        loadCommentsByPage(currentPage);
      }
    });
}

function validateCommentForm() {
  const comment = document.forms["commentForm"]["content"].value;

  if (isFieldEmpty(comment)) {
    alert("Comment cannot be empty");
    return false;
  }
}

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
    .catch((err) => {
      console.error("Error:", err);
      document.getElementById("updateStatus").innerText = "出錯了！";
    });
}

// ajax
function postComment(event) {
  event.preventDefault();

  let content = document.querySelector('input[name="content"]').value;

  fetch("/createMessage", {
    method: "POST",
    headers: {
      // "Content-Type": "application/x-www-form-urlencoded",
      "Content-Type": "application/json",
      // "User-Id" : userId
    },
    // body: `content=${content}`,
    body: JSON.stringify({
      content: content,
      // user_id: userId
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else if (data.message && data.message === "Comment added") {
        addCommentToUI(data.comment);
        // Add the new comment to the UI
        // (similar to your code that adds comments on fetching them)
      }
    });
}

function addCommentToUI(comment, prepend = true) {
  const commentsList = document.querySelector(".bulletin");
  const listItem = document.createElement("li");
  // for delete
  listItem.setAttribute("data-comment-id", comment.id);
  listItem.innerHTML = `<b>${comment.member_name} :</b> ${
    comment.content
  } <small style="color: burlywood">(${new Date(
    comment.time
  ).toLocaleString()})</small>`;

  console.log(comment.member_id);
  console.log(userId);

  if (comment.member_id == userId) {
    let deleteButton = document.createElement("button");
    deleteButton.textContent = "💩";
    deleteButton.onclick = function () {
      deleteComment(comment.id);
    };
    listItem.appendChild(deleteButton);
  }

  prepend ? commentsList.prepend(listItem) : commentsList.appendChild(listItem);
  // commentsList.insertBefore(listItem, commentList.firstChild);
}

function deleteComment(commentId) {
  if (confirm("確定要刪除這條留言嗎？")) {
    fetch("/deleteMessage", {
      method: "POST",
      headers: {
        // "Content-Type": "application/x-www-form-urlencoded",
        "Content-Type": "application/json",
        // "User-Id" : userId
      },
      // body: `comment_id=${commentId}`,
      body: JSON.stringify({
        comment_id: commentId,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          if (data.message && data.message === "Comment deleted") {
            let commentElement = document.querySelector(
              `li[data-comment-id="${commentId}"]`
            );
            if (commentElement) {
              commentElement.remove();
            }
          }
        }
      });
  }
}

let currentPage = 1;
let total_pages;

document.addEventListener("DOMContentLoaded", function () {
  if (window.location.pathname === "/member/") {
    fetchUserId();
    loadCommentsByPage(currentPage);
  }
});

function loadMoreComments() {
  fetch(`/api/getComments?page=${currentPage + 1}`) // +1 因為我們要載入下一頁
    .then((res) => res.json())
    .then((data) => {
      if (data.comments.length == 0) {
        document.getElementById("loadMoreBtn").style.display = "none";
      } else {
        currentPage = data.current_page;

        data.comments.forEach((comment) => {
          addCommentToUI(comment, false);
        });

        const loadMoreBtn = document.getElementById("loadMoreBtn");
        data.has_next
          ? (loadMoreBtn.style.display = "block")
          : (loadMoreBtn.style.display = "none");

        updatePaginationUI(data.current_page, data.total_pages);
      }
    });
}

function loadCommentsByPage(page) {
  const commentsList = document.querySelector(".bulletin");
  commentsList.innerHTML = ""; // 清空留言列表

  fetch(`/api/getComments?page=${page}`)
    .then((res) => res.json())
    .then((data) => {
      currentPage = data.current_page;

      data.comments.forEach((comment) => {
        addCommentToUI(comment, false);
      });

      const loadMoreBtn = document.getElementById("loadMoreBtn");
      data.has_next
        ? (loadMoreBtn.style.display = "block")
        : (loadMoreBtn.style.display = "none");

      updatePaginationUI(data.current_page, data.total_pages);
    });
}

// function loadComments(page) {
//   currentPage = page;

//   const commentsList = document.querySelector(".bulletin");
//   commentsList.innerHTML = "";

//   fetch(`/api/getComments?page=${currentPage}`)
//     .then((res) => res.json())
//     .then((data) => {
//       // if (data.length == 0) { //陣列，若為單一資料
//       if (data.comments.length == 0) {
//         //物件，若為分頁資料

//         // 沒有留言就隱藏按鈕
//         document.getElementById("loadMoreBtn").style.display = "none";
//       } else {
//         total_pages = data.total_pages;
//         // currentPage = data.current_page;

//         // data.forEach((comment) => {
//         data.comments.forEach((comment) => {
//           addCommentToUI(comment, false);
//         });
//         // currentPage++;
//         const loadMoreBtn = document.getElementById("loadMoreBtn");

//         data.has_next
//           ? (loadMoreBtn.style.display = "block")
//           : (loadMoreBtn.style.display = "none");

//         updatePaginationUI(currentPage, total_pages);
//       }
//     });
// }

document.getElementById("loadMoreBtn").addEventListener("click", function () {
  currentPage++;
  loadMoreComments();
});

document
  .getElementById("jumpToPage")
  .addEventListener("click", jumpToSpecifiedPage);

function updatePaginationUI(currentPage, totalPages) {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = ""; // Clear

  const startPage = currentPage - 2;
  const endPage = currentPage + 2;

  // Always show the first page if not already included in the range
  if (startPage > 1) {
    pagination.appendChild(createPageItem("1", 1)); // First page
  }

  // Show ellipsis if there's a gap between first page and the startPage
  if (startPage > 2) {
    pagination.appendChild(createPageItem("...", null)); // Ellipsis
  }

  for (
    let i = Math.max(1, startPage);
    i <= Math.min(totalPages, endPage);
    i++
  ) {
    pagination.appendChild(createPageItem(i.toString(), i, i === currentPage));
  }

  // Show ellipsis if there's a gap between endPage and the last page
  if (endPage < totalPages - 1) {
    pagination.appendChild(createPageItem("...", null)); // Ellipsis
  }

  // Always show the last page if not already included in the range
  if (endPage < totalPages) {
    pagination.appendChild(createPageItem(totalPages.toString(), totalPages)); // Last page
  }
}

function createPageItem(text, pageNumber, isCurrent = false) {
  const pageItem = document.createElement("span");
  pageItem.innerText = text;

  if (pageNumber) {
    pageItem.onclick = function () {
      loadCommentsByPage(pageNumber);
    };
  }

  if (isCurrent) {
    pageItem.classList.add("current");
  }

  return pageItem;
}

function jumpToSpecifiedPage() {
  const pageNumber = parseInt(document.getElementById("jumpToPage").value);
  if (pageNumber && pageNumber >= 1 && pageNumber <= total_pages) {
    loadComments(pageNumber); // 跳轉到指定頁碼
  } else {
    alert("請輸入有效的頁碼");
  }
}

// from flask

// function confirmDelete(commentId) {
//   if (confirm("確定要刪除這條留言嗎？")) {
//     let form = document.createElement("form");
//     form.method = "POST";
//     form.action = "/deleteMessage";

//     let input = document.createElement("input");
//     input.type = "hidden";
//     input.name = "comment_id";
//     input.value = commentId;
//     form.appendChild(input);
//     document.body.appendChild(form);
//     form.submit();
//   }
// }

// document.addEventListener("DOMContentLoaded", function () {
//   if (window.location.pathname === "/member/") {
//     //     let bodyElement = document.querySelector("body");
//     //     let userId = bodyElement.getAttribute("data-user-id");
//     //     console.log(userId);
//     //     // let userId = sessionStorage.getItem("user_id");
//     if (userId) {
//       fetch("/api/getComments")
//         .then((res) => res.json())
//         .then((data) => {
//           const commentsList = document.querySelector(".bulletin");
//           commentsList.innerHTML = "";

//           data.forEach((comment) => {
//             addCommentToUI(comment, false);
//           });
//         });
//     }
//   }
// });

// function confirmDelete(commentId) {
//   const confirmation = window.confirm("要刪除留言嗎?");
//   if (confirmation) {
//     deleteComment(commentId);
//   }
// }

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
