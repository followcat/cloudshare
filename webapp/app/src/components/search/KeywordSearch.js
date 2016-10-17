'use strict';
import React, { Component } from 'react';

import { Row, Col, Form, Input, Button } from 'antd';

class KeywordSearch extends Component {

  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    const searchText = this.props.form.getFieldValue('searchText');
    this.props.onSubmit(searchText);
  }

  render() {
    const { getFieldProps } = this.props.form;

    return (
      <Form className="center">
        <Row>
          <Col span={12} offset={6}>
            <Form.Item>
              <Input
                {...getFieldProps('searchText')}
                size="large"
              />
            </Form.Item>
          </Col>
        </Row>
        <Row>
          <Col span={2} offset={6}>
            <a href="/fastmatching">Search by sentence</a>
          </Col>
          <Col span={4} offset={2}>
            <Button
              id="sBtn"
              type="primary"
              size="large"
              onClick={this.handleClick}
              htmlType="submit"
            >
            Search
            </Button>
          </Col>
        </Row>
      </Form>
    );
  }
}

export default KeywordSearch = Form.create({})(KeywordSearch);