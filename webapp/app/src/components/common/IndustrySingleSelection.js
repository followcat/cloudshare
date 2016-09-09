'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import { Select } from 'antd';

export default class IndustrySingleSelection extends Component {
  
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Select
        width={{ width: 200 }}
        placeholder="Please select a industry"
        optionFilterProp="children"
        notFoundContent="Not found"
      >
        {this.props.industryList.map((item, index) => {
          return <Select.Option key={index} value={item}>{item}</Select.Option>
        })}
      </Select>
    );
  }
}