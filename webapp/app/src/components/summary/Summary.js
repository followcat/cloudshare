'use strict';
import React, { Component, PropTypes } from 'react';
import { Row, Col, Card } from 'antd';

const TOTAL_COLUMN = 24;  // 栅栏格一行总格子数

const groupArray = (data, number) => {
  let list = [],
      current = [];

  data.forEach(item => {
    if (Array.isArray(item.value)) {
      list.push(item);
    } else {
      current.push(item);
      if (current.length === number) {
        list.push(current);
        current = [];
      }
    }
  });

  if (current.length) {
    list.push(current);
  }

  return list;
};

class Summary extends Component {
  render() {
    const props = this.props,
          data = groupArray(props.dataSource, props.number),
          colValue = TOTAL_COLUMN / props.number;

    return (
      <Card className={props.prefixCls}>
        {data.map((dataItem, index) => {
          if (Array.isArray(dataItem)) {
            return (
              <Row key={index}>
                {dataItem.map((v, i) => {
                  return (
                    <Col
                      key={i}
                      span={colValue}
                    >
                      <Col
                        span={10}
                        className={`${props.prefixCls}-label`}
                      >
                        {`${v.name}: `}
                      </Col>  
                      <Col span={14}>
                        {v.value}
                      </Col>
                    </Col>
                  );
                })}
              </Row>
            );
          } else {
            return (
              <Row key={index}>
                <Col
                  span={5}
                  className={`${props.prefixCls}-label`}
                >
                  {`${dataItem.name}: `}
                </Col>
                <Col span={19}>
                  {dataItem.value.reverse().map((valueItem, index) => {
                    return (
                      <p key={index}>{valueItem.join(' | ')}</p>
                    );
                  })}
                </Col>
              </Row>
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
