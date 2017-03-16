'use strict';
import React, { Component, PropTypes } from 'react';

import Content from 'components/content';
import ChangePassword from 'components/change-password';

class Setting extends Component {
  render() {
    const props = this.props;

    return (
      <Content prefixCls={props.prefixCls}>
        <ChangePassword onSubmit={props.onSubmit}/>
      </Content>
    );
  }
}

Setting.defaultProps = {
  prefixCls: 'cs-setting',
  onSubmit() {},
};

Setting.propTypes = {
  onSubmit: PropTypes.func,
};

export default Setting;
