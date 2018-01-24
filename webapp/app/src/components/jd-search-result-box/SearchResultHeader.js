'use strict';
import React, { Component } from 'react';

import { Affix, Row, Col } from 'antd';

class SearchResultHeader extends Component {
  render() {
    const cols = [{
      title: '姓名',
      span: 3
    }, {
      title: '性别',
      span: 1
    }, {
      title: '年龄',
      span: 1
    }, {
      title: '婚姻状况',
      span: 2
    }, {
      title: '学历',
      span: 3
    }, {
      title: '院校',
      span: 3
    }, {
      title: '职位',
      span: 3
    }, {
      title: '最近公司',
      span: 4
    }, {
      title: '上传人',
      span: 3
    },];

    return (
      <Affix>
        <Row className="cs-search-result-header">
          <Col span={1}></Col>
          {cols.map((item, index) => {
            return <Col className="header-cell" span={item.span} key={index}>{item.title}</Col>;
          })}
        </Row>
      </Affix>
    );
  }
}

export default SearchResultHeader;
