'use strict';
import React, { Component } from 'react';

import { Affix, Row, Col } from 'antd';

class SearchResultHeader extends Component {
  render() {
    const cols = [{
      title: '匹配度',
      span: 1
    },{
      title: '姓名',
      span: 2
    }, {
      title: '性别',
      span: 1
    }, {
      title: '年龄',
      span: 1
    }, {
      title: '婚姻状态',
      span: 2
    }, {
      title: '学历',
      span: 3
    }, {
      title: '院校',
      span: 3
    }, {
      title: '职位名称',
      span: 3
    }, {
      title: '任职公司',
      span: 4
    }, {
      title: '上传人',
      span: 3
    },];
    const colsB = [{
      title: '姓名',
      span: 2
    }, {
      title: '性别',
      span: 1
    }, {
      title: '年龄',
      span: 1
    }, {
      title: '婚姻状态',
      span: 2
    }, {
      title: '学历',
      span: 3
    }, {
      title: '院校',
      span: 3
    }, {
      title: '职位名称',
      span: 3
    }, {
      title: '任职公司',
      span: 4
    }, {
      title: '上传人',
      span: 3
    },];
    const headerItem = this.props.header ? cols : colsB;
    return (
      <Affix>
        <Row className="cs-search-result-header">
          <Col span={1}></Col>
          {headerItem.map((item, index) => {
            return <Col className="header-cell" span={item.span} key={index}>{item.title}</Col>;
          })}
        </Row>
      </Affix>
    );
  }
}

SearchResultHeader.defaultProps = {
  header: false
};

export default SearchResultHeader;
