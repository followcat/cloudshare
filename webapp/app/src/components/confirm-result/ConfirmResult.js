'use strict';
import React, { Component, PropTypes } from 'react';
import { Table } from 'antd';

class ConfirmResult extends Component {
  render() {
    const {
      prefixCls,
      columns,
      dataSource
    } = this.props;

    return (
      <div className={prefixCls}>
        <Table
          columns={columns}
          dataSource={dataSource}
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
