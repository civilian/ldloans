import axios from 'axios';

// Add a request interceptor
axios.interceptors.request.use( config => {
  const user = JSON.parse(localStorage.getItem('user'));

  if(user && user.auth_token){
    const token = 'Bearer ' + user.auth_token;
    config.headers.Authorization =  token;
  }

  return config;
});

class BackendService {
  async getUserData() {
    return await axios.get("/auth/status");
  }

  createLoanApplication = (business_name, requested_amount, tax_id) => {
    return axios.post("/loan/apply", {business_name, requested_amount, tax_id});
  }
}

export default new BackendService();