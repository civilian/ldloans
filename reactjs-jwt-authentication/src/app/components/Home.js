import React, { Component } from 'react';
import AppNavbar from './AppNavbar';
import { Link } from 'react-router-dom';
import { Button, Container, Alert } from 'reactstrap';

import AuthenticationService from '../services/AuthenticationService';

class Home extends Component {

  constructor(props) {
    super(props);
    this.state = {
      user: undefined,
      login: false
    };
  }

  componentDidMount() {
    const user = AuthenticationService.getCurrentUser();

    if (user) {
      this.setState({
        user: user,
        login: true
      });
    }
  }

  render() {

    const user = this.state.user;
    return (
      <div>
        <AppNavbar/>
        <Container fluid>
          <div style={{marginTop:"20px"}}>
            <Alert variant="primary">
              <h2>Ldloans Loans Application</h2>
              { (!this.state.login)? (
                  <Button color="success"><Link to="/signin"><span style={{color:"white"}}>Login</span></Link></Button>
                ):(<br></br>)
              }
            </Alert>
          </div>
        </Container>
      </div>
    );
  }
}

export default Home;