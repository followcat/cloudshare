'use strict';
import React, { Component, PropTypes } from 'react';

import Cell from './Cell';

class BasicInfoItem extends Component {
  render() {
    const { itemInfo, labelCls, dataSource, dataIndex } = this.props;
    
    return (
      <div className="cs-item-row">
        <label className={`cs-item-row-label ${labelCls}`}>{itemInfo.title}</label>
        <Cell
          span={20}
          dataSource={dataSource}
          dataIndex={dataIndex}
          onSave={this.props.onSave}
        />
      </div>
    );
  }
}

BasicInfoItem.defaultProps = {
  labelCls: '',
  contentCls: '',
  itemInfo: {},
  dataSource: {},
  onSave() {}
};

BasicInfoItem.propTypes = {
  labelCls: PropTypes.string,
  contentCls: PropTypes.string,
  itemInfo: PropTypes.object,
  dataSource: PropTypes.object,
  dataIndex: PropTypes.string,
  onSave: PropTypes.func
};

export default BasicInfoItem;
