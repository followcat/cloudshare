'use strict';
import React, { Component, PropTypes } from 'react';

import Animation from './Animation';
import Mask from './Mask';
import Panel from './Panel';

class SiderPanelPortal extends Component {
  render() {
    const props = this.props;

    return (
      <div>
        <Animation
          visible={props.visible}
          transitionName="mask"
        >
          <Mask
            maskClosable={props.maskClosable}
            onClose={props.onClose}
          />
        </Animation>
        <Animation
          visible={props.visible}
          transitionName={props.transitionName}
          transitionEnterTimeout={props.transitionEnterTimeout}
          transitionLeaveTimeout={props.transitionLeaveTimeout}
        >
          <Panel
            title={props.title}
            width={props.width}
            position={props.position}
            onClose={props.onClose}
            children={props.children}
          />
        </Animation>
      </div>
    );
  }
}

SiderPanelPortal.defaultProps = {
  visible: false,
  transitionName: 'panel',
  transitionEnterTimeout: 600,
  transitionLeaveTimeout: 500,
};

SiderPanelPortal.propTypes = {
  visible: PropTypes.bool,
  transitionName: PropTypes.string,
  transitionEnterTimeout: PropTypes.number,
  transitionLeaveTimeout: PropTypes.number,
};

export default SiderPanelPortal;
