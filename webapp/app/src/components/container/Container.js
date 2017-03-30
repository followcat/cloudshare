'use strict';
import React, { Component, PropTypes } from 'react';

class Container extends Component {
  render() {
    const {
      prefixCls,
      children
    } = this.props;

    return(
      <div className={prefixCls}>
        <div className={`${prefixCls}-wrapper`}>
            {children}
        </div>
      </div>
    );
  }
}

Container.defaultProps = {
  prefixCls: 'cs-container'
};

Container.propTypes = {
  prefixCls: PropTypes.string,
  children: PropTypes.element
};

export default Container;
