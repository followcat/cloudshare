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
    return (
      <div
        className="sider-panel-mask"
        onClick={this.handleClick}  
      >
      </div>
    );
  }
}

Mask.defaultProps = {
  maskClosable: true,
  onClose() {}
};

Mask.propTypes = {
  maskClosable: PropTypes.bool,
  onClose: PropTypes.func,
};

export default Mask;
