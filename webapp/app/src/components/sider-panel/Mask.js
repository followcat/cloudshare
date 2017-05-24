'use strict';
import React, { Component, PropTypes } from 'react';

class Mask extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    if (this.props.maskClosable) {
      this.props.onClose();
    }
  }

  render() {
    const { prefixCls } = this.props;

    return (
      <div className={prefixCls} onClick={this.handleClick} />
    );
  }
}

Mask.defaultProps = {
  prefixCls: 'sider-panel-mask',
  maskClosable: true,
  onClose() {}
};

Mask.propTypes = {
  prefixCls: PropTypes.string,
  maskClosable: PropTypes.bool,
  onClose: PropTypes.func,
};

export default Mask;
