import React, { Component } from 'react';
import { Collapse, Nav, Navbar, NavbarBrand, NavbarToggler, NavbarText, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';

import { withRouter } from 'react-router-dom';

import AuthenticationService from '../services/AuthenticationService';

class AppNavbar extends Component {
  constructor(props) {
    super(props);
    this.state = {isOpen: false};
    this.toggle = this.toggle.bind(this);

    this.state = {
      showLoanApplications: false,
      showCreateLoanApplications: false,
      email: undefined,
      login: false
    };
  }

  componentDidMount() {
    const user = AuthenticationService.getCurrentUser();

    if (user) {
      const roles = [];
      this.setState({
        showLoanApplications: true,
        showCreateLoanApplications: true,
        login: true,
        email: user.email
      });
    }
  }

  signOut = () => {
    AuthenticationService.signOut();
    this.props.history.push('/home');
    window.location.reload();
  }

  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }

  render() {
    return <Navbar color="dark" dark expand="md">
      <NavbarBrand tag={Link} to="/home">Ldloans</NavbarBrand>
      <Nav className="mr-auto">
        <NavLink href="/home">Home</NavLink>
        {/* {this.state.showLoanApplications && <NavLink href="/loanApplications">Loan Applications</NavLink>} */}
        {this.state.showCreateLoanApplications && <NavLink href="/createLoanApplications">Create Loan Application</NavLink>}
      </Nav>
      <NavbarToggler onClick={this.toggle}/>
      <Collapse isOpen={this.state.isOpen} navbar>
        {
          this.state.login ? (
            <Nav className="ml-auto" navbar>
              <NavItem>
                  <NavbarText>
                    Signed in as: <a href="/profile">{this.state.email}</a>
                  </NavbarText>
              </NavItem>
              <NavItem>
                <NavLink href="#" onClick={this.signOut}>LogOut</NavLink>
              </NavItem>
            </Nav>                 
          ) : (
            <Nav className="ml-auto" navbar>
              <NavItem>
                <NavLink href="/signin">Login</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/signup">SignUp</NavLink>
              </NavItem>
            </Nav>
          )
        }
      </Collapse>
    </Navbar>;
  }
}

export default withRouter(AppNavbar);