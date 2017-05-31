'use strict';
import React, { Component, PropTypes } from 'react';

import Cell from './Cell';

class BasicInfoItem extends Component {
  render() {
    const {
      itemInfo,
      labelCls,
      dataSource,
      dataIndex,
      editStatus
    } = this.props;
    
    return (
      <div className="cs-item-row">
        <label className={`cs-item-row-label ${labelCls}`}>{itemInfo.title}</label>
        <Cell
          span={20}
          itemInfo={itemInfo}
          dataSource={dataSource}
          dataIndex={dataIndex}
          editStatus={editStatus}
          onUpdateFieldValues={this.props.onUpdateFieldValues}
          onUpdateDeleteList={this.props.onUpdateDeleteList}
        />
      </div>
    );
  }
}

BasicInfoItem.defaultProps = {
  labelCls: '',
  itemInfo: {},
  dataSource: {},
};

BasicInfoItem.propTypes = {
  editStatus: PropTypes.bool,
  labelCls: PropTypes.string,
  itemInfo: PropTypes.object,
  dataSource: PropTypes.object,
  dataIndex: PropTypes.string,
  onUpdateFieldValues: PropTypes.func,
  onUpdateDeleteList: PropTypes.func
};

export default BasicInfoItem;
