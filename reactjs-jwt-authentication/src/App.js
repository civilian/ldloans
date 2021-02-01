import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './App.css';
import Home from './app/components/Home';
import Profile from './app/components/Profile';
import CreateLoanApplication from './app/components/CreateLoanApplication';
import SignUp from './app/components/SignUp';
import Login from './app/components/Login';

class App extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route path='/' exact={true} component={Home}/>
          <Route path='/home' exact={true} component={Home}/>
          <Route path='/profile' exact={true} component={Profile}/>
          <Route path='/createLoanApplications' exact={true} component={CreateLoanApplication}/>
          <Route path='/signin' exact={true} component={Login}/>
          <Route path='/signup' exact={true} component={SignUp}/>  
        </Switch>
      </Router>
    )
  }
}

export default App;