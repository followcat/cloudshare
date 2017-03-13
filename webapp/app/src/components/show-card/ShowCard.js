'use strict';
import React, { Component, PropTypes } from 'react';

class ShowCard extends Component {
  render() {
    return (
      <div className={`${this.props.prefixCls}`}>
        {this.props.children}
      </div>
    );
  }
}

ShowCard.defaultProps = {
  prefixCls: 'cs-show-card',
};

ShowCard.propTypes = {
  prefixCls: PropTypes.string,
  children: PropTypes.element
};

export default ShowCard;
