'use strict';
import React, { Component, PropTypes } from 'react';
import { Row, Col, Card } from 'antd';

const TOTAL_COLUMN = 24;  // 栅栏格一行总格子数

class Summary extends Component {
  render() {
    const props = this.props,
          colValue = TOTAL_COLUMN / props.number;

    return (
      <Card>
        {props.dataSource.map((dataItem, index) => {
          if (Array.isArray(dataItem.value)) {
            return (
              <Row key={index}>
                <Col
                  span={4}
                  className={`${props.prefixCls}-label`}
                >
                  {`${dataItem.name}: `}
                </Col>
                <Col span={20}>
                  {dataItem.value.map((valueItem, index) => {
                    return (
                      <p key={index}>{valueItem.join(' | ')}</p>
                    );
                  })}
                </Col>
              </Row>
            );
          } else {
            return (
              <Col
                key={index}
                span={colValue}
              >
                <Col
                  span={8}
                  className={`${props.prefixCls}-label`}
                >
                  {`${dataItem.name}: `}
                </Col>  
                <Col span={16}>
                  {dataItem.value}
                </Col>
              </Col>
            );
          }
        })}
      </Card>
    );
  }
}

Summary.defaultProps = {
  prefixCls: 'cs-summary',
  number: 2,  // 每一行默认由2个数据项组成
  dataSource: [],
};

Summary.propTypes = {
  prefixCls: PropTypes.string,
  number: PropTypes.number,
  dataSource: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string,
    value: PropTypes.oneOf([PropTypes.string, PropTypes.array]),
  })),
};

export default Summary;
