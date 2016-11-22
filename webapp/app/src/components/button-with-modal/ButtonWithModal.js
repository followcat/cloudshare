'use strict';
import React, { Component, PropTypes } from 'react';
import { Button, Modal } from 'antd';

class ButtonWithModal extends Component {
  render() {
    const props = this.props;

    return (
      <div className="cs-button-with-modal">
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
          comfirmLoading={props.comfirmLoading}
          title={props.modalTitle}
          width={props.modalWidth}
          okText={props.modalOkText}
          cancelText={props.modalCancelText}
          style={props.modalStyle}
          wrapClassName={props.modalWrapClassName}
          onOk={props.onModalOk}
          onCancel={props.onModalCancel}
        >
          {props.children}
        </Modal>
      </div>
    );
  }
}

ButtonWithModal.defaultProps = {
  buttonType: 'ghost',
  buttonLoading: false,
  buttonText: '',
  onButtonClick() {},
  visible: false,
  comfirmLoading: false,
  modalOkText: 'Ok',
  modalCancelText: 'Cancel',
  onModalOk() {},
  onModalCancel() {},
};  

ButtonWithModal.propTypes = {
  buttonStyle: PropTypes.object,
  buttonType: PropTypes.string,
  buttonSize: PropTypes.string,
  buttonLoading: PropTypes.bool,
  buttonText: PropTypes.string,
  onButtonClick: PropTypes.func,
  visible: PropTypes.bool,
  comfirmLoading: PropTypes.bool,
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
