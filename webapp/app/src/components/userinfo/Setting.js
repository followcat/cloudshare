'use strict';
import React, { Component } from 'react';

import ChangePassword from '../common/ChangePassword';

export default class Setting extends Component {
  render() {
    return (
      <div>
        <div className="pwd-content">
          <ChangePassword onSubmit={this.props.onSubmitChangePassword}/>
        </div>
      </div>
    );
  }
}