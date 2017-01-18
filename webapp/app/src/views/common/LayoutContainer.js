'use strict';
import React, { Component, PropTypes } from 'react';

class LayoutContainer extends Component {
  render() {
    return (
      <div className={this.props.prefixCls}>
        {this.props.children}
      </div>
    );
  }
}

LayoutContainer.defaultProps = {
  prefixCls: 'cs-layout-container'
};

LayoutContainer.propTypes = {
  prefixCls: PropTypes.string,
  children: PropTypes.element
};

export default LayoutContainer;
