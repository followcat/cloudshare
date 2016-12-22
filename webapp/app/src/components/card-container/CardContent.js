'use strict';
import React, { Component, PropTypes } from 'react';

class CardContent extends Component {
  render() {
    const props = this.props;

    return (
      <div className="cs-card-content">
        <div className="cs-card-content-header">
          <span className="cs-card-content-title">{props.title}</span>
        </div>
        {props.children}
      </div>
    );
  }
}

CardContent.defaultProps = {
  title: '',
};

CardContent.propTypes = {
  title: PropTypes.string,
};

export default CardContent;
