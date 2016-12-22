'use strict';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';
import SiderPanelPortal from './SiderPanelPortal';

class SiderPanel extends Component {
  constructor() {
    super();
    this.renderPortal = this.renderPortal.bind(this);
    this.beforeOpen = this.beforeOpen.bind(this);
    this.afterClose = this.afterClose.bind(this);
  }

  componentDidMount() {
    this.node = document.createElement('div');
    document.body.appendChild(this.node);
    this.renderPortal();
  }

  componentWillUpdate() {
    this.beforeOpen();
  }

  componentDidUpdate() {
    this.renderPortal();

    if (!this.props.visible) {
      this.afterClose();
    }
    
  }

  componentWillUnmount() {
    ReactDOM.unmountComponentAtNode(this.node);
    document.body.removeChild(this.node);
  }

  renderPortal() {
    ReactDOM.unstable_renderSubtreeIntoContainer(this, <SiderPanelPortal {...this.props} />, this.node);
  }

  beforeOpen() {
    const scrollWidth = window.innerWidth - document.body.clientWidth;

    document.body.style.paddingRight = `${scrollWidth}px`;
    document.body.style.overflow = 'hidden';
  }

  afterClose() {
    document.body.removeAttribute('style');
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
