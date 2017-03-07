'use strict';
import React, { Component, PropTypes } from 'react';

class CardContainer extends Component {
  render() {
    return (
      <div className="cs-card-container">
        {this.props.children}
      </div>
    );
  }
}

CardContainer.defaultProps = {
  children: null,
};

CardContainer.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.element),
    PropTypes.element
  ])
};

export default CardContainer;
