import React, { Component } from 'react';

import ChangePassword from '../common/ChangePassword';

export default class Setting extends Component {
  render() {
    return (
      <div>
        <div className="cs-layout-content" ref="contentDiv">
          <div className="pwd-content">
            <ChangePassword />
          </div>
        </div>
      </div>
    );
  }
}