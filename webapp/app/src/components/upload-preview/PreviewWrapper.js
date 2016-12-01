'use strict';
import React, { Component, PropTypes } from 'react';

class PreviewWrapper extends Component {
  render() {
    const props = this.props;
    let classes = props.prefixCls;

    if (props.actived) {
      classes = `${classes} cs-upload-preview-active`;
    }

    return (
      <div className={classes}>
        {props.children}
      </div>
    );
  }
}

PreviewWrapper.defaultProps = {
  prefixCls: 'cs-upload-preview',
  actived: false,
};

PreviewWrapper.propTypes = {
  prefixCls: PropTypes.string,
  actived: PropTypes.bool,
};

export default PreviewWrapper;
