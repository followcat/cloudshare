'use strict';
import React, { Component, PropTypes } from 'react';

class NavigationItem extends Component {
  render() {
    const props = this.props;

    return (
      <div className={`${props.prefixCls}`}>
        {props.render()}
      </div>
    );
  }
}

NavigationItem.defaultProps = {
  prefixCls: 'cs-nav-item',
};

NavigationItem.propTypes = {
  prefixCls: PropTypes.string,
  render: PropTypes.func,
};

export default NavigationItem;
