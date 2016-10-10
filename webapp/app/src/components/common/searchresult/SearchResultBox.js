'use strict';
import React, { Component, PropTypes } from 'react';

import { Spin } from 'antd';

import SearchResultHeader from './SearchResultHeader';
import SearchResultItem from './SearchResultItem';
import SearchResultPagination from './SearchResultPagination';

import classNames from 'classnames';
import './searchresult.less';

export default class SearchResultBox extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const classSet = classNames({
      'cs-search-result': true,
      'showed': this.props.visible === true,
      'hidden': this.props.visible === false,
    });

    return (
      <div className={classSet}>
        <Spin spinning={this.props.spinning}>
          <SearchResultHeader />
          {this.props.dataSource.map((item, index) => {
            return (
              <SearchResultItem
                {...item}
                key={index}
                selection={this.props.selection}
                onToggleSelection={this.props.onToggleSelection}
              />
            );
          })}
        </Spin>
        <SearchResultPagination
          total={this.props.total}
          onSwitchPage={this.props.onSwitchPage}
        />
      </div>
    );
  }
}

SearchResultBox.propTypes = {
  visible: PropTypes.bool,
  spinning: PropTypes.bool,
  total: PropTypes.number,
  dataSource: PropTypes.array,
  onSwitchPage: PropTypes.func,
  onToggleSelection: PropTypes.func,
};