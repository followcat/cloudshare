'use strict';
import React, { Component, PropTypes } from 'react';

import Cell from './Cell';

class AdditionalInfoItem extends Component {
  render() {
    const { itemInfo, dataSource, dataIndex } = this.props;

    return (
      <div className="cs-item-row">
        <label className="cs-item-row-label extra-label">{itemInfo.title}</label>
        <Cell
          span={20}
          dataSource={dataSource}
          dataIndex={dataIndex}
          onSave={this.props.onSave}
          onRemove={this.props.onRemove}
        />
      </div>
    );
  }
}

AdditionalInfoItem.defaultProps = {
  dataSource: {},
  itemInfo: {},
  onSave() {},
  onRemove() {}
};

AdditionalInfoItem.propTypes = {
  dataSource: PropTypes.object,
  dataIndex: PropTypes.string,
  itemInfo: PropTypes.object,
  onSave: PropTypes.func,
  onRemove: PropTypes.func
};

export default AdditionalInfoItem;
