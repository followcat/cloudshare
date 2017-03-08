'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon } from 'antd';

class Tag extends Component {
  render() {
    return (
      <div className="cs-tag">
        <span className="cs-tag-text">{this.props.text}</span>
        <Icon type="cross-circle-o" onClick={this.props.onClick} />
      </div>
    );
  }
}

Tag.propTypes = {
  text: PropTypes.string,
  onClick: PropTypes.func
};

export default Tag;
