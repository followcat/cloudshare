import React, { Component } from 'react';

import { Modal, message } from 'antd';

import 'whatwg-fetch';
import marked from 'marked';

export default class Feature extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      mdContent: null,
    };
    this.handleShowModal = this.handleShowModal.bind(this);
    this.handleOk = this.handleOk.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleShowModal() {
    fetch(`/api/feature`)
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          visible: true,
          mdContent: { __html: marked(json.data) },
        });
      }
    });
  }

  handleOk() {
    this.setState({
      visible: false,
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  render() {
    return (
      <div>
        <div className="feature" onClick={this.handleShowModal}>
          Feature
        </div>
        <Modal title="Feature"
          wrapClassName="vertical-center-modal"
          visible={this.state.visible}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
          okText="OK"
          cancelText="Cancel"
        >
          <div dangerouslySetInnerHTML={this.state.mdContent}></div>
        </Modal>
      </div>
    );
  }
}