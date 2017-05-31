'use strict';
import React, { Component, PropTypes } from 'react';

import ChangePassword from 'components/change-password';

import { message } from 'antd';

import { resetPassword } from 'request/password';
import { signOut } from 'request/sign';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class Setting extends Component {
  constructor() {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(fieldValue) {
    const params = {
      oldpassword: fieldValue.oldPassword,
      newpassword: fieldValue.reNewPassword,
    };

    resetPassword(params, (json) => {
      if (json.code === 200) {
        message.success(language.RESET_PWD_SUCCESS_MSG);
        setTimeout(() => {
          signOut((response) => {
            if (response.code === 200) {
              localStorage.removeItem('token');
              localStorage.removeItem('user');
              location.href = response.redirect_url;
            }
          });
        }, 1000);
      } else {
        message.error(language.RESET_PWD_FAIL_MSG);
      }
    });
  }

  render() {
    const props = this.props;

    return (
      <div className={props.className} style={props.style}>
        <ChangePassword onSubmit={this.handleSubmit} />
      </div>
    );
  }
}

Setting.defaultProps = {
  style: {}
};

Setting.propTypes = {
  style: PropTypes.object,
  className: PropTypes.string,
  onSubmit: PropTypes.func,
};

export default Setting;
