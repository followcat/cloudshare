'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Card } from 'antd';

import { URL } from 'URL';

class History extends Component {
  render() {
    const {
      storage,
      title,
      bordered,
      bodyStyle
    } = this.props;

    return (
      <Card
        title={title}
        bordered={bordered}
        bodyStyle={bodyStyle}
      >
        <div className="cs-history">
          {storage.map((item) => {
            return (
              <Row key={item.id} className="history-row">
                <Col span={8}>{item.time}</Col>
                <Col span={16}>
                  <a href={URL.getResumeURL(item.id)} target="_blank">{item.name}</a>
                </Col>
              </Row>
            );
          })}
        </div>
      </Card>
    );
  }
}

History.defaultProps = {
  title: '浏览历史',
  storage: [],
  bordered: true,
};

History.propTypes = {
  storage: PropTypes.array,
  title: PropTypes.string,
  bordered: PropTypes.bool,
  bodyStyle: PropTypes.object,
};

export default History;
