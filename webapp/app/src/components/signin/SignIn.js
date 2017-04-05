'use strict';
import React, { Component, PropTypes } from 'react';
import { Card } from 'antd';
import SignInForm from './SignInForm';

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
  title: 'Sign in',
  bordered: true,
  className: '',
  style: {},
  prefixCls: 'cs-signin'
};

SignIn.propTypes = {
  title: PropTypes.string,
  bordered: PropTypes.bool,
  className: PropTypes.string,
  style: PropTypes.object,
};

export default SignIn;
