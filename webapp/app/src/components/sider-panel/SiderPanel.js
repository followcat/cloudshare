'use strict';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';
import SiderPanelPortal from './SiderPanelPortal';

class SiderPanel extends Component {
  constructor() {
    super();
    this.renderPortal = this.renderPortal.bind(this);
  }

  componentDidMount() {
    this.node = document.createElement('div');
    document.body.appendChild(this.node);
    this.renderPortal();
  }

  componentDidUpdate() {
    this.renderPortal();
  }

  componentWillUnmount() {
    ReactDOM.unmountComponentAtNode(this.node);
    document.body.removeChild(this.node);
  }

  renderPortal() {
    ReactDOM.unstable_renderSubtreeIntoContainer(this, <SiderPanelPortal {...this.props} />, this.node);
  }

  render() {
    return null;
  }
}

SiderPanel.defaultProps = {
  visible: false,
  maskClosable: true,
  transitionName: 'panel',
  transitionEnterTimeout: 600,
  transitionLeaveTimeout: 500,
  title: '',
  width: null,
  position: 'right',
  onClose() {}
};

SiderPanel.propTypes = {
  visible: PropTypes.bool,
  maskClosable: PropTypes.bool,
  transitionName: PropTypes.string,
  transitionEnterTimeout: PropTypes.number,
  transitionLeaveTimeout: PropTypes.number,
  title: PropTypes.string,
  width: PropTypes.number,
  position: PropTypes.string,
  onClose: PropTypes.func,
};

export default SiderPanel;
