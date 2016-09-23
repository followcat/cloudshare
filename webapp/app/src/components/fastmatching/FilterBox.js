'use strict';
import React, { Component, PropTypes } from 'react';

import { Card } from 'antd';
import FilterInfo from './FilterInfo';
import FilterForm from './FilterForm';

export default class FilterBox extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const style = {
      width: 1080,
      height: 'auto',
      margin: '20px auto',
    };

    return (
      <Card style={style}>
        <div className="pd-lr-30">
          <FilterInfo {...this.props} />
          <FilterForm {...this.props} />
        </div>
      </Card>
    );
  }
}

FilterBox.propTypes ={
  total: PropTypes.number,
};