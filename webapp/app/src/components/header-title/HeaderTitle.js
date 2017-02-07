import React, { Component, PropTypes } from 'react';
import { Row, Col } from 'antd';

class HeaderTitle extends Component {
  render() {
    const { prefixCls, dataSource } = this.props;

    return (
      <div className={prefixCls}>
        <Row>
          {dataSource.map(item => {
            return (
              <Col
                key={item.key}
                className={`${prefixCls}-cell`}
                span={item.span}
              >
                {item.text}
              </Col>
            );
          })}
        </Row>
      </div>
    );
  }
}

HeaderTitle.defaultProps = {
  prefixCls: 'cs-header-title',
  dataSource: []
};

HeaderTitle.propTypes = {
  span: PropTypes.number,
  prefixCls: PropTypes.string,
  dataSource: PropTypes.array
};

export default HeaderTitle;
