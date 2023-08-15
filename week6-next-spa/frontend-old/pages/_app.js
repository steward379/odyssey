import axios from "axios";

axios.post("/backendURL/signIn", { username, password }).then((response) => {
  if (response.data.status === "success") {
    // Handle success
  } else {
    // Handle error
  }
});
