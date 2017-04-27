'use strict';
import React, { Component, PropTypes } from 'react';

import SearchResultHeader from './SearchResultHeader';
import SearchResultItem from './SearchResultItem';
import SearchResultPagination from 'components/search-result-box/SearchResultPagination';

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
      postData,
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
            postData={postData}
            onClick={this.props.onClick}
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
      total
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
        <SearchResultPagination
          current={current}
          total={total}
          onSwitchPage={this.props.onSwitchPage}
        />
      </div>
    );
  }
}

SearchResultBox.defaultProps = {
  prefixCls: 'cs-search-result'
};

SearchResultBox.propTypes = {
  prefixCls: PropTypes.string,
  type: PropTypes.string,
  visible: PropTypes.bool,
  spinning: PropTypes.bool,
  current: PropTypes.number,
  total: PropTypes.number,
  dataSource: PropTypes.array,
  educationExperienceText: PropTypes.string,
  workExperienceText: PropTypes.string,
  selection: PropTypes.array,
  postData: PropTypes.object,
  foldText: PropTypes.string,
  unfoldText: PropTypes.string,
  onSwitchPage: PropTypes.func,
  onClick: PropTypes.func
};

export default SearchResultBox;
