'use strict';
import React, { Component, PropTypes } from 'react';

import FilterForm from './FilterForm';
import FilterInfo from './FilterInfo';

import { Card } from 'antd';

class FilterCard extends Component {
  render() {
    const { prefixCls } = this.props;

    return (
      <Card className={prefixCls}>
        <FilterInfo {...this.props} />
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
