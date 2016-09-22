'use strict';
import React, { Component, PropTypes } from 'react';

import { Card } from 'antd';
import FilterInfo from './FilterInfo';
import FilterForm from './FilterForm';

export default class FilterBox extends Component {

  render() {
    const style = {
      width: 1080,
      height: 'auto',
      margin: '20px auto',
    };

    return (
      <Card style={style}>
        <div className="pd-lr-30">
          <FilterInfo />
          <FilterForm />
        </div>
      </Card>
    );
  }
}