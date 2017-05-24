'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon } from 'antd';

class Tag extends Component {
  render() {
    const { prefixCls, text } = this.props;

    return (
      <div className={prefixCls}>
        <span className={`${prefixCls}-text`}>{text}</span>
        <Icon type="cross-circle-o" onClick={this.props.onClick} />
      </div>
    );
  }
}

Tag.defaultProps = {
  prefixCls: 'cs-tag'
};

Tag.propTypes = {
  prefixCls: PropTypes.string,
  text: PropTypes.string,
  onClick: PropTypes.func
};

export default Tag;
