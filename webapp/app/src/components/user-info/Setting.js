'use strict';
import React, { Component, PropTypes } from 'react';
import Content from '../content';
import ChangePassword from '../change-password';

class Setting extends Component {
  render() {
    const props = this.props;

    return (
      <Content prefixCls={props.settingPrefixCls}>
        <ChangePassword onSubmit={props.onSubmit}/>
      </Content>
    );
  }
}

Setting.defaultProps = {
  onSubmit() {},
};

Setting.propTypes = {
  settingPrefixCls: PropTypes.string,
  onSubmit: PropTypes.func,
};

export default Setting;
