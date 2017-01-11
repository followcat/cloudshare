'use strict';
import React, { Component, PropTypes } from 'react';

class LayoutHeader extends Component {
  render() {
    return (
      <div className="cs-layout-header">
        <div className="cs-layout-wrapper">
          <div className="cs-layout-logo">
            <img src={this.props.logoImg} alt="Logo" />
          </div>
          {this.props.children}
        </div>
      </div>
    );
  }
}

LayoutHeader.propTypes = {
  logoImg: PropTypes.string,
  children: PropTypes.element
};

export default LayoutHeader;
