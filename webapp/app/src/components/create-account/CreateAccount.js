'use strict';
import React, { Component, PropTypes } from 'react';

import CreateAccountForm from './CreateAccountForm';

import { Card } from 'antd';

class CreateAccount extends Component {
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
        style={{border: '1px solid #9e9797'}}
      >
        <CreateAccountForm {...props} />
      </Card>
    );
  }
}

CreateAccount.defaultProps = {
  prefixCls: 'cs-createaccount',
  title: 'CreateAccount',
  bordered: true,
  className: '',
  style: {}
};

CreateAccount.propTypes = {
  prefixCls: PropTypes.string,
  title: PropTypes.string,
  bordered: PropTypes.bool,
  className: PropTypes.string,
  style: PropTypes.object,
};

export default CreateAccount;
