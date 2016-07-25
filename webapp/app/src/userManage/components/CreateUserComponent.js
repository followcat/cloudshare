import React from 'react';
import ReactDOM from 'react-dom';

import RaisedButton from 'material-ui/RaisedButton';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';

export default class CreateUserComponent extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      open: false,
      userName: '',
      password: '',
      confirmPassword: ''
    };
  }

  handleOpen() {
    this.setState({
      open: true
    });
  }

  handleClose() {
    this.setState({
      open: false
    });
  }

  handleSubmit() {
    this.props.onCreateUserSubmit({
      userName: this.state.userName,
      password: this.state.password,
      confirmPassword: this.state.confirmPassword
    });
    this.handleClose();
    this.setState({
      userName: '',
      password: '',
      confirmPassword: ''
    });
  }

  setValue(field, event) {
    let object = {};
    object[field] = event.currentTarget.value;
    this.setState(object);
  }

  render() {
    const actions = [
      <FlatButton
        label="Cancel"
        primary={true}
        onTouchTap={this.handleClose.bind(this)}
      />,
      <FlatButton 
        label="Submit"
        primary={true}
        onTouchTap={this.handleSubmit.bind(this)}
      />
    ];
    return (
      <div>
      <RaisedButton 
        label="Crate New User" 
        backgroundColor="#337ab7"
        onTouchTap={this.handleOpen.bind(this)}
        labelStyle={{color: "#fff"}}
      />
      <Dialog
        title="Create a new user"
        actions={actions}
        modal={false}
        open={this.state.open}
        onRequestClose={this.handleClose.bind(this)}
      >
      <TextField
        hintText="Please input your user name."
        floatingLabelText="User Name"
        fullWidth="true"
        value={ this.state.userName }
        onChange={ this.setValue.bind(this, 'userName' )}
      />
      <br />
      <TextField
        hintText="Please input your password."
        floatingLabelText="Password"
        type="password"
        fullWidth="true"
        value={ this.state.password }
        onChange={ this.setValue.bind(this, 'password' )}
      />
      <br />
      <TextField
        hintText="Please input your confirm password."
        floatingLabelText="Confirm Password"
        type="password"
        fullWidth="true"
        value={ this.state.confirmPassword }
        onChange={ this.setValue.bind(this, 'confirmPassword' )}
      />
      </Dialog>
      </div>
    );
  }
}