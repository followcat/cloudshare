'use strict';
import React, { Component, PropTypes } from 'react';
import { Row, Col } from 'antd';

class HistoryItem extends Component {
  render() {
    const props = this.props,
          rowStyle = {
            paddingTop: 8,
            paddingBottom: 8,
            borderBottomWidth: 1,
            borderBottomStyle: 'dashed',
            borderBottomColor: 'rgb(236, 236, 236)',
          };
    return (
      <Row style={rowStyle}>
        <Col span={8}>{props.time}</Col>
        <Col span={16}>
          <a href={props.id} target="_block">{props.name}</a>
        </Col>
      </Row>
    );
  }
}

export default HistoryItem;
