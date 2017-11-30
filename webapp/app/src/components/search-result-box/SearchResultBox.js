'use strict';
import React, { Component, PropTypes } from 'react';

import SearchResultHeader from './SearchResultHeader';
import SearchResultItem from './SearchResultItem';
import SearchResultPagination from './SearchResultPagination';

import { Spin } from 'antd';

import ColorGrad from 'utils/color-grad';

import classNames from 'classnames';

class SearchResultBox extends Component {
  constructor() {
    super();
    this.state = {
      gradient: []
    };
    this.getResultDOMRender = this.getResultDOMRender.bind(this);
  }

  componentDidMount() {
    const colorGrad = new ColorGrad();
    this.setState({
      gradient: colorGrad.gradient(),
    });
  }

  getResultDOMRender() {
    const {
      educationExperienceText,
      workExperienceText,
      dataSource,
      selection,
      foldText,
      unfoldText
    } = this.props;

    const type = this.props.type || 'default';
    if (type === 'default') {
      return dataSource.map((item, index) => {
        return (
          <SearchResultItem
            {...item}
            key={index}
            type={type}
            educationExperienceText={educationExperienceText}
            workExperienceText={workExperienceText}
            foldText={foldText}
            unfoldText={unfoldText}
          />
        );
      });
    } else {
      return dataSource.map((item, index) => {
        return (
          <SearchResultItem
            {...item}
            key={index}
            educationExperienceText={educationExperienceText}
            workExperienceText={workExperienceText}
            foldText={foldText}
            unfoldText={unfoldText}
            selection={selection}
            onToggleSelection={this.props.onToggleSelection}
            gradient={this.state.gradient}
          />
        );
      });
    }
  }

  
  render() {
    const {
      prefixCls,
      visible,
      spinning,
      current,
      total,
      showPagination
    } = this.props;

    const classSet = classNames({
      [`${prefixCls}`]: true,
      'showed': visible === true,
      'hidden': visible === false,
    });

    return (
      <div className={classSet}>
        <Spin spinning={spinning}>
          <SearchResultHeader />
          {this.getResultDOMRender()}
        </Spin>
        { showPagination ?
        <SearchResultPagination
          current={current}
          total={total}
          onSwitchPage={this.props.onSwitchPage}
        />
        : null
        }
      </div>
    );
  }
}

SearchResultBox.defaultProps = {
  prefixCls: 'cs-search-result',
  showPagination: true
};

SearchResultBox.propTypes = {
  prefixCls: PropTypes.string,
  type: PropTypes.string,
  visible: PropTypes.bool,
  showPagination: PropTypes.bool,
  spinning: PropTypes.bool,
  current: PropTypes.number,
  total: PropTypes.number,
  dataSource: PropTypes.array,
  educationExperienceText: PropTypes.string,
  workExperienceText: PropTypes.string,
  selection: PropTypes.array,
  foldText: PropTypes.string,
  unfoldText: PropTypes.string,
  onSwitchPage: PropTypes.func,
  onToggleSelection: PropTypes.func
};

export default SearchResultBox;
