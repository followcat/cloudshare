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
        bordered={props.bordered}
        className={classes}
        style={{border: '5px solid #e9e9e9', 'border-radius': '10px'}}
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
