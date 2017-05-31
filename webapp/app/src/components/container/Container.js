'use strict';
import React, { Component, PropTypes } from 'react';

class Container extends Component {
  render() {
    const {
      prefixCls,
      className,
      children
    } = this.props;

    let classes = prefixCls;
    if (className) {
      classes += ` ${className}`;
    }

    return(
      <div className={classes}>
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
  className: PropTypes.string,
  children: PropTypes.element
};

export default Container;
