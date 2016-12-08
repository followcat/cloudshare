'use strict';
import React, { Component, PropTypes } from 'react';
import { Icon } from 'antd';
import classNames from 'classnames';

class Panel extends Component {
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
      >
        <div className="close">
          <Icon
            type="cross"
            onClick={props.onClose}
          />
        </div>
        <div className="sider-panel-header">
          {props.title}
        </div>
        <div className="sider-panel-content">
          {props.children}
        </div>
      </div>
    );
  }
}

Panel.defaultProps = {
  title: '',
  position: 'right',
  visible: false,
  onClose() {},
};

Panel.propTypes = {
  title: PropTypes.string,
  width: PropTypes.number,
  children: PropTypes.arrayOf(PropTypes.element),
  position: PropTypes.oneOf(['left', 'right']),
  onClose: PropTypes.func,
};

export default Panel;
