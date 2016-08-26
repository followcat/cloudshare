import React, { Component } from 'react';

import { message } from 'antd';

import ChangePassword from '../common/ChangePassword';

message.config({
  top: 66,
  duration: 3,
});

export default class Setting extends Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(e) {
    //Submit fetch
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