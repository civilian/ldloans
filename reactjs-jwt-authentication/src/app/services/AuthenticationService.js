import axios from "axios";

class AuthenticationService {
  signin = (email, password) => {
      return axios.post("/auth/login", {email, password})
        .then(response => {
          if (response.data.auth_token) {
            localStorage.setItem("user", JSON.stringify(response.data));
          }
          return response.data;
        })
        .catch(err => {
          console.log(err);
          throw err;
        });
  }

  signOut() {
    localStorage.removeItem("user");
  }

  register = async(email, password) => {
    return axios.post("/auth/register", {
      email,
      password
    });
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  }
}

export default new AuthenticationService();