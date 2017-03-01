import React, { Component, PropTypes } from 'react';
import { Row, Col } from 'antd';

import classNames from 'classnames';

class HeaderTitle extends Component {
  render() {
    const {
      prefixCls,
      dataSource,
      position
    } = this.props;

    const cls = classNames({
      [`${prefixCls}-cell`]: true,
      'text-center': position === 'center',
      'text-left': position === 'left'
    });

    return (
      <div className={prefixCls}>
        <Row>
          {dataSource.map(item => {
            return (
              <Col
                key={item.key}
                className={cls}
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
  dataSource: [],
  position: 'center'
};

HeaderTitle.propTypes = {
  span: PropTypes.number,
  prefixCls: PropTypes.string,
  dataSource: PropTypes.array,
  position: PropTypes.string
};

export default HeaderTitle;
