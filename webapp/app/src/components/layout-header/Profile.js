'use strict';
import React, { Component, PropTypes } from 'react';
import { Icon, Badge } from 'antd';

import { messagesNotify } from 'request/message'

class Profile extends Component {
    state = {
    count: 0,
  }

  componentWillMount(){
    messagesNotify ((json) => {
        if(json.code === 200) {
          this.setState({
            count : json.result.invited_customer+json.result.unread_chat
            })
          }
        })
  }

  render() {
    return (
      <div className="cs-layout-profile">
        <div className="cs-layout-profile-icon">
          <Icon type="user" />
        </div>
        <div className="cs-layout-profile-content">
        <Badge count={this.state.count}>
          {this.props.children}
         </Badge> 
        </div>
      </div>
    );
  }
}

export default Profile;