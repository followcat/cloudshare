'use strict';
import React, { Component, PropTypes } from 'react';

class Container extends Component {
  render() {
    const props = this.props;

    return(
      <div className={`${props.prefixCls}`}>
        <div className={`${props.prefixCls}-wrapper`}>
            {props.children}
        </div>
      </div>
    );
  }
}

Container.defaultProps = {
  prefixCls: 'cs-container',
};

Container.propTypes = {
  prefixCls: PropTypes.string,
};

export default Container;
