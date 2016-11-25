'use strict';
import React, { Component, PropTypes } from 'react';

class AlertPrompt extends Component {
  render() {
    const props = this.props;

    return (
      <div className={`${props.prefixCls} ${props.prefixCls}-${props.type}`}>
        <div className={`${props.prefixCls}-title`}>{props.title}</div>
        <div className={`${props.prefixCls}-content`}>
          {props.children}
        </div>
      </div>
    );
  }
}

AlertPrompt.defaultProps = {
  prefixCls: 'cs-alert-prompt',
  type: 'info',
  title: '',
};

AlertPrompt.propTypes = {
  prefixCls: PropTypes.string,
  type: PropTypes.string,
  title: PropTypes.string,
};

export default AlertPrompt;
