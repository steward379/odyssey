import axios from "axios";

const API_ENDPOINT = "http://localhost:5000"; // Flask server address

const instance = axios.create({
  baseURL: API_ENDPOINT,
});

export const signUp = (data) => {
  // return axios.post(`${API_ENDPOINT}/signUp`, data);
  return instance.post(`/signUp`, data);
};

export const signOut = () => {
  return instance.get(`/signOut`);
};

export default instance;
