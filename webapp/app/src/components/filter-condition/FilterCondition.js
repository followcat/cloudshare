'use strict';
import React, { Component, PropTypes } from 'react';

import { Select, Button, Input, Icon } from 'antd';

import cloneDeep from 'lodash/cloneDeep';
import remove from 'lodash/remove';
import findIndex from 'lodash/findIndex';

import Condition from './Condition';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class FilterCondition extends Component {
  constructor(props) {
    super(props);
    this.state = {
      options: this.props.options,
      filterData: [{data:['name',''],index:0}]
    };
    this.updateFilterCondition = this.updateFilterCondition.bind(this);
    this.handleAddFilterCondition = this.handleAddFilterCondition.bind(this);
    this.handleFilterClick = this.handleFilterClick.bind(this);
  }

  componentDidMount() {
  }

  updateFilterCondition(index, dataIndex, fieldValue = null) {
    const { filterData } = this.state;
    let datas = cloneDeep(filterData),
        i = findIndex(datas, (v) => v.index === index);
    if(i>=0)
    switch(dataIndex) {
      case 'key':
        datas[i].data[0] = fieldValue;
        break;
      case 'value':
        datas[i].data[1] = fieldValue;
        break;
      case 'delete':
        remove(datas, (v) => v.index === index);
        break;
    }

    this.setState({
      filterData: datas
    });
  }

  handleAddFilterCondition(e) {
    e.preventDefault();
    const { filterData } = this.state;
    let datas = cloneDeep(filterData),
        len = datas.length;
    
    if (len > 0) {
      datas.push({
        index: datas[len - 1].index + 1,
        data: []
      });
    } else {
      datas.push({
        index: 0,
        data: []
      });
    }
  
    this.setState({
      filterData: datas
    });
  }

  handleFilterClick() {
    const { filterData } = this.state;
    (!this.isFilterValueNull()) && this.props.getDataSource(filterData);
  }

  isFilterValueNull() {
    const { filterData } = this.state;

    let data = filterData.map(v => v.data);

    for (var i = 0, len = data.length; i < len; i++) {
      if (typeof data[i][1] === 'undefined' || data[i][1] === '') {
        return true;
      }
    }

    return false;
  }

  render() {
    const { filterData, options } = this.state;
    const { prefixCls } =this.props;
    return (
          <div className={prefixCls}>
            <label className={`${prefixCls}-label`}>过滤条件：</label>
            {filterData.map((item) => {
              return (
              <Condition
                  key={item.index}
                  index={item.index}
                  options={options}
                  updateFilterCondition={this.updateFilterCondition}
              />
              )
            })}
            <a onClick={this.handleAddFilterCondition}>添加条件</a>
            <Button onClick={this.handleFilterClick}>{language.SUBMIT}</Button>
          </div>
    );
  }
}

FilterCondition.defaultProps = {
  prefixCls: 'cs-filter-condition',
  options: []
}

FilterCondition.propTypes = {
  index: PropTypes.number,
  prefixCls: PropTypes.String,
  updateFilterCondition: PropTypes.func
};

export default FilterCondition;
