'use strict';
import React, { Component, PropTypes } from 'react';

import SignInForm from './SignInForm';

import { Card } from 'antd';

class SignIn extends Component {
  render() {
    const props = this.props;
    let classes = props.prefixCls;
    if (props.className) {
      classes += props.className;
    }

    return (
      <Card
        title={props.title}
        bordered={props.bordered}
        className={classes}
        style={props.style}
      >
        <SignInForm {...props} />
      </Card>
    );
  }
}

SignIn.defaultProps = {
  prefixCls: 'cs-signin',
  title: 'Sign in',
  bordered: true,
  className: '',
  style: {}
};

SignIn.propTypes = {
  prefixCls: PropTypes.string,
  title: PropTypes.string,
  bordered: PropTypes.bool,
  className: PropTypes.string,
  style: PropTypes.object,
};

export default SignIn;
