'use strict';
import React, { Component } from 'react';

import { Button } from 'antd';

export default class ResumeComfirm extends Component {
  
  constructor(props) {
    super(props);
    this.handleComfirmClick = this.handleComfirmClick.bind(this);
  }

  handleComfirmClick() {
    const fieldsValue = this.props.form.getFieldsValue();
    let value = Object.assign(fieldsValue, { id: this.props.id });
    this.props.onComfirmUpload(value);
  }

  render() {
    return (
      <Button
        loading={this.props.loading}
        onClick={this.handleComfirmClick}
      >
        Comfirm
      </Button>
    );
  }
}