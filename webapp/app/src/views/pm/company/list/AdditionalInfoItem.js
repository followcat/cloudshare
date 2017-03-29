'use strict';
import React, { Component, PropTypes } from 'react';

import Cell from './Cell';

class AdditionalInfoItem extends Component {
  render() {
    const {
      itemInfo,
      dataSource,
      dataIndex,
      editStatus
    } = this.props;

    return (
      <div className="cs-item-row">
        <label className="cs-item-row-label extra-label">{itemInfo.title}</label>
        <Cell
          span={20}
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

AdditionalInfoItem.defaultProps = {
  dataSource: {}
};

AdditionalInfoItem.propTypes = {
  editStatus: PropTypes.bool,
  dataSource: PropTypes.object,
  dataIndex: PropTypes.string,
  itemInfo: PropTypes.object,
  onUpdateFieldValues: PropTypes.func,
  onUpdateDeleteList: PropTypes.func
};

export default AdditionalInfoItem;
