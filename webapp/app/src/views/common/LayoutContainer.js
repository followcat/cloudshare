'use strict';
import React, { Component, PropTypes } from 'react';

class LayoutContainer extends Component {
  render() {
    const { prefixCls, style } = this.props;

    return (
      <div className={prefixCls} style={style}>
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
  style: PropTypes.object,
  children: PropTypes.oneOfType([PropTypes.element, PropTypes.arrayOf(PropTypes.element)])
};

export default LayoutContainer;
