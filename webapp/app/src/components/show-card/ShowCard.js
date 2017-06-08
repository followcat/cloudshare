'use strict';
import React, { Component, PropTypes } from 'react';

class ShowCard extends Component {
  render() {
    const { prefixCls, children } = this.props;

    return (
      <div className={prefixCls}>
        {children}
      </div>
    );
  }
}

ShowCard.defaultProps = {
  prefixCls: 'cs-show-card',
};

ShowCard.propTypes = {
  prefixCls: PropTypes.string,
  children: PropTypes.oneOfType([PropTypes.element, PropTypes.arrayOf(PropTypes.element)])
};

export default ShowCard;
