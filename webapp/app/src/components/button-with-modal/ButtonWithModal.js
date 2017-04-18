'use strict';
import React, { Component, PropTypes } from 'react';
import { Button, Modal } from 'antd';

class ButtonWithModal extends Component {
  render() {
    const props = this.props;

    return (
      <div className={props.prefixCls}>
        <Button
          style={props.buttonStyle}
          type={props.buttonType}
          size={props.buttonSize}
          loading={props.buttonLoading}
          onClick={props.onButtonClick}
        >
          {props.buttonText}
        </Button>
        <Modal
          visible={props.visible}
          title={props.modalTitle}
          width={props.modalWidth}
          style={props.modalStyle}
          wrapClassName={props.modalWrapClassName}
          onCancel={props.onModalCancel}
          footer={[
            <Button size="large" onClick={props.onModalCancel}>{props.modalCancelText}</Button>,
            <Button
              type="primary"
              size="large"
              loading={props.confirmLoading}
              onClick={props.onModalOk}
              disabled={props.disabled}
            >
              {props.modalOkText}
            </Button>
          ]}
        >
          {props.children}
        </Modal>
      </div>
    );
  }
}

ButtonWithModal.defaultProps = {
  prefixCls: 'cs-button-with-modal',
  buttonType: 'ghost',
  buttonLoading: false,
  buttonText: '',
  onButtonClick() {},
  visible: false,
  confirmLoading: false,
  disabled: false,
  modalOkText: 'Ok',
  modalCancelText: 'Cancel',
  onModalOk() {},
  onModalCancel() {}
};

ButtonWithModal.propTypes = {
  prefixCls: PropTypes.string,
  buttonStyle: PropTypes.object,
  buttonType: PropTypes.string,
  buttonSize: PropTypes.string,
  buttonLoading: PropTypes.bool,
  buttonText: PropTypes.string,
  onButtonClick: PropTypes.func,
  visible: PropTypes.bool,
  confirmLoading: PropTypes.bool,
  disabled: PropTypes.bool,
  modalTitle: PropTypes.string,
  modalWidth: PropTypes.number,
  modalOkText: PropTypes.string,
  modalCancelText: PropTypes.string,
  modalStyle: PropTypes.object,
  modalWrapClassName: PropTypes.string,
  onModalOk: PropTypes.func,
  onModalCancel: PropTypes.func,
  modalContent: PropTypes.element,
};

export default ButtonWithModal;
