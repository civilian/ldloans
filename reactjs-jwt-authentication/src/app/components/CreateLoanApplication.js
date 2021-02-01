import React, { Component } from 'react';
import AppNavbar from './AppNavbar';
import { Container } from 'reactstrap';
import { Button, Form, FormGroup, Input, Label, Row, Col } from "reactstrap";
import { Alert } from "react-bootstrap"

import Authentication from '../services/AuthenticationService'
import BackendService from '../services/BackendService';

const validEmailRegex = RegExp(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i);

const validateForm = (errors) => {
  let valid = true;
  Object.values(errors).forEach(
    (val) => val.length > 0 && (valid = false)
  );
  return valid;
}

class CreateLoanApplication extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      business_name: "",
      requested_amount: undefined,
      tax_id: "",
      message: "",
      successful: false,
      validForm: true,
      errors: {
        business_name: '',
        passwrequested_amountord: '',
        tax_id: '',
      }
    };
  }

  changeHandler = (event) => {
    const { name, value } = event.target;
  
    let errors = this.state.errors;  
    this.setState({errors, [name]: value}, ()=> {
        console.log(errors)
    })  
  }

  createLoanApplication = (e) => {
    e.preventDefault();
    const valid = validateForm(this.state.errors);
    this.setState({validForm: valid});
    if(valid){
      BackendService.createLoanApplication(
        this.state.business_name,
        this.state.requested_amount,
        this.state.tax_id
      ).then(
        response => {
          var successful = true
          if (response.data.data.status == 'fail'){
            successful = false
          }
          this.setState({
            message: response.data.data.message,
            successful: successful
          });
        },
        error => {
          console.log("Fail! Error = " + error.toString());
          console.log(error)
          this.setState({
            successful: false,
            message: error.toString()
          });
        }
      );  
    }
  }

  render() {
    const title = <h2>Create Loan Application</h2>;
    const errors = this.state.errors;

    let alert = "";

    if(this.state.message){
      if(this.state.successful){
        alert = (
                  <Alert variant="success">
                    {this.state.message}
                  </Alert>
                );
      }else{
        alert = (
                  <Alert variant="danger">
                    {this.state.message}
                  </Alert>
                );
      }
    }

    return ( 
      <div>
        <AppNavbar/>
        <Container fluid>
          <Row>
          <Col sm="12" md={{ size: 4, offset: 4 }}>
          {title}
            <Form onSubmit={this.createLoanApplication}>
              <FormGroup controlId="formBusinessName">
                <Label for="business_name">Business Name</Label>
                <Input required
                  type="text" 
                  placeholder="Enter Business Name"
                  name="business_name" id="business_name"
                  value={this.state.business_name}
                  autoComplete="business_name"
                  onChange={this.changeHandler}
                />
                {
                  errors.business_name && ( 
                      <Alert variant="danger">
                        {errors.business_name}
                      </Alert>
                    )
                }
              </FormGroup>

              <FormGroup controlId="formRequestedAmount">
                <Label for="requested_amount">Requested Amount</Label>
                <Input required 
                  type="number" step='0.0001'
                  placeholder="Enter Requested Amount"
                  name="requested_amount" id="requested_amount"
                  value={this.state.requested_amount}
                  autoComplete="requested_amount"
                  onChange={this.changeHandler}
                />
                {
                  errors.requested_amount && ( 
                      <Alert key="errorsrequested_amount" variant="danger">
                        {errors.requested_amount}
                      </Alert>
                    )
                }
              </FormGroup>

              <FormGroup controlId="formTaxId">
                <Label for="tax_id">Tax Id</Label>
                <Input required 
                  type="text" 
                  placeholder="Enter Tax Id"
                  name="tax_id" id="tax_id"
                  value={this.state.tax_id}
                  autoComplete="tax_id"
                  onChange={this.changeHandler}
                />
                {
                  errors.tax_id && ( 
                      <Alert key="errorstax_id" variant="danger">
                        {errors.requested_amount}
                      </Alert>
                    )
                }
              </FormGroup>

              <Button variant="primary" type="submit">
                Create
              </Button>
              {
                !this.state.validForm && (
                  <Alert key="validForm" variant="danger">
                    Please check the inputs again!
                  </Alert>
                )
              }

              {alert}
            </Form>
            </Col>
          </Row>
        </Container>
      </div>);
  }
}

export default CreateLoanApplication;