'use strict';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';

import { Icon } from 'antd';

import classNames from 'classnames';
import getStyle from 'utils/get-style';

class Panel extends Component {
  constructor() {
    super();
    this.setContentScroll = this.setContentScroll.bind(this);
  }

  componentDidMount() {
    this.setContentScroll();
  }

  componentDidUpdate() {
    this.setContentScroll();
  }

  setContentScroll() {
    const container = ReactDOM.findDOMNode(this.refs.container),
          header = ReactDOM.findDOMNode(this.refs.header),
          content = ReactDOM.findDOMNode(this.refs.content);

    const containerHeight = container.offsetHeight,
          headerHeight = header.offsetHeight,
          contentHeight = content.offsetHeight,
          containerPaddingTop = parseInt(getStyle(container, 'paddingTop')),
          containerPaddingBottom = parseInt(getStyle(container, 'paddingBottom'));

    let maxContentHeight = containerHeight - headerHeight - containerPaddingTop - containerPaddingBottom;
    if (contentHeight > maxContentHeight) {
      content.style.overflowY = 'scroll';
      content.style.maxHeight = `${maxContentHeight}px`;
    }
  }

  render() {
    const props = this.props;
    let style = {};

    if (props.width) {
      style = { width: props.width };
    }

    const classes = classNames({
      'sider-panel-wrapper': true,
      'sider-panel-left': props.position === 'left',
      'sider-panel-right': props.position === 'right',
    });

    return (
      <div
        tabIndex="-1"
        className={classes}
        style={style}
        ref="container"
      >
        <div className="close">
          <Icon
            type="cross"
            onClick={props.onClose}
          />
        </div>
        <div
          className="sider-panel-header"
          ref="header"
        >
          {props.title}
        </div>
        <div
          className="sider-panel-content"
          ref="content"
        >
          {props.children}
        </div>
      </div>
    );
  }
}

Panel.defaultProps = {
  prefixCls: 'sider-panel-wrapper',
  title: '',
  position: 'right',
  visible: false,
  onClose() {},
};

Panel.propTypes = {
  title: PropTypes.string,
  width: PropTypes.number,
  position: PropTypes.oneOf(['left', 'right']),
  onClose: PropTypes.func,
};

export default Panel;
