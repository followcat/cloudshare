'use strict';
import React, { Component } from 'react';

import { Row, Col, Checkbox, Button, Input, Form } from 'antd';

class ResumeToolMenu extends Component {

  constructor(props) {
    super(props);

    this.state = {
      checked: false,
      name: '',
      source: '',
    };

    this.handleSwitchChange = this.handleSwitchChange.bind(this);
    this.hangdleSubmit = this.hangdleSubmit.bind(this);
  }

  handleSwitchChange(e) {
    this.setState({
      checked: e.target.checked,
    });
  }

  hangdleSubmit(e) {
    e.preventDefault();
    const fieldValue = this.props.form.getFieldsValue();
    this.props.onModifyTitle(fieldValue);
  }

  render() {
    const { getFieldProps } = this.props.form,
          style = this.state.checked ? { display: 'block' } : { display: 'none' };

    return (
      <div>
        <div className="tool-menu pd-lr-8">
          <Checkbox onChange={this.handleSwitchChange}>Switch to Modify Title</Checkbox>
          <Button type="ghost" size="small">Download</Button>
          <Button type="ghost" size="small" style={{ marginLeft: 4 }}>Add English CV</Button>
        </div>
        <Form className="title-form pd-lr-8" style={style}>
          <Row>
            <Col span={8} className="title-wrapper">
              <Form.Item
                label="ID"
                prefixCls="title"
              >
                <Input size="small" value={this.props.dataSource.id} readOnly={true} />
              </Form.Item>   
            </Col>
            <Col span={8} className="title-wrapper">
              <Form.Item
                label="Name"
                prefixCls="title"
              >
                <Input
                  {...getFieldProps('name', { initialValue: this.props.dataSource.name })}
                  type="text"
                  size="small"
                />
              </Form.Item>
            </Col>
            <Col span={8} className="title-wrapper">
              <Form.Item
                
                label="Source"
                prefixCls="title"
              >
                <Input
                  {...getFieldProps('origin', { initialValue: this.props.dataSource.origin })}
                  type="text"
                  size="small"
                />
              </Form.Item>
            </Col>
          </Row>
          <Row>
            <Col span={2} offset={11}>
              <Button size="small" onClick={this.hangdleSubmit}>Submit</Button>
            </Col>
          </Row>
        </Form>
      </div>
    );
  }
}

export default ResumeToolMenu = Form.create({})(ResumeToolMenu);
