'use strict';
import React, { Component, PropTypes } from 'react';

import FilterForm from './FilterForm';

import { Card } from 'antd';

class FilterCard extends Component {
  render() {
    const { prefixCls } = this.props;

    return (
      <Card className={prefixCls} style={{ margin: '0px auto'}}>
        <FilterForm {...this.props} />
      </Card>
    );
  }
}

FilterCard.defaultProps = {
  prefixCls: 'cs-filter-card'
};

FilterCard.propTypes = {
  prefixCls: PropTypes.string
};

export default FilterCard;
