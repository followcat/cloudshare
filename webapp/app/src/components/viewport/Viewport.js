'use strict';
import React, { Component, PropTypes } from 'react';

class Viewport extends Component {
  render() {
    return (
      <div
        className={this.props.prefixCls}
        style={this.props.style}
      >
        {this.props.children}
      </div>
    );
  }
}

Viewport.defaultProps = {
  prefixCls: 'viewport',
  style: null
};

Viewport.propTypes = {
  prefixCls: PropTypes.string,
  style: PropTypes.object,
};

export default Viewport;
