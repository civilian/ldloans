import React, { Component } from 'react';
import AppNavbar from './AppNavbar';
import { Link } from 'react-router-dom';
import { Button, Container } from 'reactstrap';
import { Alert } from "react-bootstrap"

import AuthenticationService from '../services/AuthenticationService';
import BackendService from '../services/BackendService';

class Profile extends Component {

  constructor(props) {
    super(props);
    this.state = {
      user: undefined,
      data: undefined
    };
  }

  componentDidMount() {
    const user = AuthenticationService.getCurrentUser();
    BackendService.getUserData()
      .then( response => {
        console.log(response);
        this.setState({
          content: response.data.data,
          user: user
        })
      } , error => {
        console.log(error);
        this.setState({
          user: user,
          error: error.message.toString(),
        }); 
      });
  }

  render() {
    let userInfo = "";
    const user = this.state.user;

    const userLogged = (u) => { return u && u.auth_token;}

    if ( userLogged(user) && this.state.content) { // user logged and no errors

      console.log(this.state.content)
      userInfo = (
                <div style={{marginTop:"20px"}}>
                  <Alert variant="info">
                    <h2>User Info</h2>
                    <ul>
                      <li>User id: {this.state.content.user_id}</li>
                      <li>Email: {this.state.content.email}</li>
                      <li>Admin: {this.state.content.admin.toString()}</li>
                      <li>Registered on: {this.state.content.registered_on.toString()}</li>
                      <li>Access Token: {user.auth_token}</li>
                    </ul>
                  </Alert>
                </div>
              );
    } else if(userLogged(user)) { // user logged but errors
      userInfo = (
        <div style={{marginTop:"20px"}}>
          <Alert variant="danger">
            <h2>User Info</h2>
            <ul>
              <li>Error ocurred please log in again.</li>
              <li>User Access Token: {this.state.user.auth_token}</li>
            </ul>
          </Alert>
        </div>
      );
    } else { // not login
      userInfo = <div style={{marginTop:"20px"}}>
                    <Alert variant="primary">
                      <h2>Profile Component</h2>
                      <Button color="success"><Link to="/signin"><span style={{color:"white"}}>Login</span></Link></Button>
                    </Alert>
                  </div>
    }

    return (
      <div>
        <AppNavbar/>
        <Container fluid>
        {userInfo}
        </Container>
      </div>
    );
  }
}

export default Profile;