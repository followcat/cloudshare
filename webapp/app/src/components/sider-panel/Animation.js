'use strict';
import React, { Component, PropTypes } from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';

class Animation extends Component {
  render() {
    const props = this.props;
    let children = null;

    if (props.visible) {
      children = props.children;
    }

    return (
      <ReactCSSTransitionGroup
        transitionName={props.transitionName}
        transitionEnterTimeout={props.transitionEnterTimeout}
        transitionLeaveTimeout={props.transitionLeaveTimeout}
      >
        {children}
      </ReactCSSTransitionGroup>
    );
  }
}

Animation.defaultProps = {
  visible: false,
  transitionEnterTimeout: 1000,
  transitionLeaveTimeout: 1000,
};

Animation.propTypes = {
  visible: PropTypes.bool,
  transitionEnterTimeout: PropTypes.number,
  transitionLeaveTimeout: PropTypes.number,
};

export default Animation;
