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
    const {
      prefixCls,
      className,
      style,
      text,
      title,
      visible,
      width,
      cancelText,
      modalStyle,
      wrapClassName,
      footer
    } = this.props;

    let classes = prefixCls,
        wrapCls = 'cs-feature-wrap';

    if (className) {
      classes = `${prefixCls} ${className}`;
    }

    if (wrapClassName) {
      wrapCls += ` ${wrapClassName}`;
    }

    return (
      <div
        className={classes}
        style={style}
        onClick={this.props.onClick}
      >
        <div className={`${prefixCls}-text`}>
          {text}
        </div>
        <Modal
          title={title}
          visible={visible}
          style={modalStyle}
          width={width}
          wrapClassName={wrapCls}
          cancelText={cancelText}
          footer={footer}
          onCancel={this.props.onCancel}
        >
          <div dangerouslySetInnerHTML={{__html: this.getMarkup()}}></div>
        </Modal>
      </div>
    );
  }
}

Feature.defaultProps = {
  prefixCls: 'cs-feature',
  wrapClassName: '',
  className: '',
  text: '更新日志',
  dataSource: '',
  title: '更新日志',
  visible: false,
  width: 520,
  okText: '',
  cancelText: '取消',
  style: {},
  modalStyle: {},
  onClick() {},
  onOk() {},
  onCancel() {}
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
  footer: PropTypes.string
};

export default Feature;
