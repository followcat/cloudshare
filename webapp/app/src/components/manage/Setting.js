import React, { Component } from 'react';

import { message } from 'antd';

import ChangePassword from '../common/ChangePassword';

message.config({
  top: 66,
  duration: 3,
});

export default class Setting extends Component {
  constructor() {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(pwd) {
    fetch(`/api/accounts/${localStorage.user}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        oldpassword: pwd.oldPwd,
        newpassword: pwd.reNewPwd,
      }),
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        message.success(json.message);
        setTimeout(() => {
          fetch(`/api/session`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
              'Authorization': `Basic ${localStorage.token}`,
            },
          })
          .then((response) => {
            return response.json();
          })
          .then((json) => {
            if (json.code === 200) {
              localStorage.removeItem('token');
              localStorage.removeItem('user');
              location.href = json.redirect_url;
            }
          });
        }, 1000);
        
      } else {
        message.error(json.message);
      }
    });
  }

  render() {
    return (
      <div>
        <div className="pwd-content">
          <ChangePassword onSubmit={this.handleSubmit}/>
        </div>
      </div>
    );
  }
}