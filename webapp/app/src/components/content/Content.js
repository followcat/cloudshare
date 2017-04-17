'use strict';
import React, { Component, PropTypes } from 'react';

class Content extends Component {
  render() {
    const {
      prefixCls,
      children
    } = this.props;

    return (
      <div className={prefixCls}>
        {children}
      </div>
    );
  }
}

Content.defaultProps = {
  prefixCls: 'cs-layout-content'
};

Content.propTypes = {
  prefixCls: PropTypes.string,
  children: PropTypes.element
};

export default Content;
