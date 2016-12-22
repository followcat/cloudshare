'use strict';
import React, { Component, PropTypes } from 'react';
import { Icon } from 'antd';

class Profile extends Component {
  render() {
    return (
      <div className="cs-layout-profile">
        <div className="cs-layout-profile-icon">
          <Icon type="user" />
        </div>
        <div className="cs-layout-profile-content">
          {this.props.children}
        </div>
      </div>
    );
  }
}

export default Profile;