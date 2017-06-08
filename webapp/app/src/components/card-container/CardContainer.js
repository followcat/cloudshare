'use strict';
import React, { Component, PropTypes } from 'react';

class CardContainer extends Component {
  render() {
    const { prefixCls, children } = this.props;

    return (
      <div className={prefixCls}>
        {children}
      </div>
    );
  }
}

CardContainer.defaultProps = {
  prefixCls: 'cs-card-container',
  children: null,
};

CardContainer.propTypes = {
  prefixCls: PropTypes.string,
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.element),
    PropTypes.element
  ])
};

export default CardContainer;
