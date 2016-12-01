'use strict';
import React, { Component, PropTypes } from 'react';
import { Table } from 'antd';

class ConfirmResult extends Component {
  render() {
    const props = this.props;

    return (
      <div className={`${props.prefixCls}`}>
        <Table
          columns={props.columns}
          dataSource={props.dataSource}
          pagination={false}
          bordered={true}
        />
      </div>
    );
  }
}

ConfirmResult.defaultProps = {
  prefixCls: 'cs-confirm-result',
};

ConfirmResult.propTypes = {
  prefixCls: PropTypes.string,
  columns: PropTypes.array,
  dataSource: PropTypes.array,
};

export default ConfirmResult;
