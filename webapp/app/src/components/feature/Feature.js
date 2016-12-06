'use strict';
import React, { Component, PropTypes } from 'react';
import { Modal, message } from 'antd';
import marked from 'marked';

class Feature extends Component {
  constructor() {
    super();
    this.getMarkup = this.getMarkup.bind(this);
  }

  getMarkup() {
    return marked(this.props.dataSource);
  }

  render() {
    const props = this.props;
    let classes = props.prefixCls;
    if (props.className) {
      classes = `${props.prefixCls} ${props.className}`;
    }

    return (
      <div
        className={classes}
        style={props.style}
        onClick={props.onClick}
      >
        <div className={`${props.prefixCls}-text`}>
          {props.text}
        </div>
        <Modal
          title={props.title}
          visible={props.visible}
          onOk={props.onOk}
          onCancel={props.onCancel}
          width={props.width}
          okText={props.okText}
          cancelText={props.cancelText}
          style={props.modalStyle}
          wrapClassName={props.wrapClassName}
        >
          <div dangerouslySetInnerHTML={{__html: this.getMarkup()}}></div>
        </Modal>
      </div>
    );
  }
}

Feature.defaultProps = {
  className: '',
  text: 'Feature',
  onClick() {},
  dataSource: '',
  title: 'Feature',
  visible: false,
  onOk() {},
  onCancel() {},
  width: 520,
  okText: 'OK',
  cancelText: 'Cancel',
  style: {},
  modalStyle: {},
  wrapClassName: '',
  prefixCls: 'cs-feature',
};

Feature.propTypes = {
  className: PropTypes.string,
  text: PropTypes.string,
  onClick: PropTypes.func,
  dataSource: PropTypes.string,
  title: PropTypes.string,
  visible: PropTypes.bool,
  onOk: PropTypes.func,
  onCancel: PropTypes.func,
  width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  okText: PropTypes.string,
  cancelText: PropTypes.string,
  style: PropTypes.object,
  modalStyle: PropTypes.object,
  wrapClassName: PropTypes.string,
  prefixCls: PropTypes.string,
};

export default Feature;
