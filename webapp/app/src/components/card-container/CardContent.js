'use strict';
import React, { Component, PropTypes } from 'react';

class CardContent extends Component {
  render() {
    const {
      prefixCls,
      title,
      children
    } = this.props;

    return (
      <div className={prefixCls}>
        <div className={`${prefixCls}-header`}>
          <span className={`${prefixCls}-title`}>{title}</span>
        </div>
        {children}
      </div>
    );
  }
}

CardContent.defaultProps = {
  prefixCls: 'cs-card-content',
  title: ''
};

CardContent.propTypes = {
  prefixCls: PropTypes.string,
  title: PropTypes.string,
  children: PropTypes.element
};

export default CardContent;
