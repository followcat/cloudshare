'use strict';
import React, { Component, PropTypes } from 'react';

class Content extends Component {
  render() {
    return (
      <div className={this.props.prefixCls}>
        {this.props.children}
      </div>
    );
  }
}

Content.defaultProps = {
  prefixCls: 'cs-layout-content',
};

Content.propTypes = {
  prefixCls: PropTypes.string,
};

export default Content;
