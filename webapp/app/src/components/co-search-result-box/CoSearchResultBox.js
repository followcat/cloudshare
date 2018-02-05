'use strict';
import React, { Component, PropTypes } from 'react';

import SearchResultHeader from './SearchResultHeader';
import SearchResultItem from './SearchResultItem';

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
    const { startColor, endColor } = this.props,
          colorGrad = new ColorGrad();
    this.setState({
      gradient: startColor && endColor ? colorGrad.gradient(startColor,endColor) : colorGrad.gradient(),
    });
  }

  getResultDOMRender() {
    const {
      educationExperienceText,
      workExperienceText,
      searchText,
      dataSource,
      selection,
      foldText,
      unfoldText
    } = this.props;

      return dataSource.map((item, index) => {
        return (
          <SearchResultItem
            dataSource={item}
            key={index}
            searchText={searchText}
            foldText={foldText}
            unfoldText={unfoldText}
            gradient={this.state.gradient}/>
        );
      });
    }
  
  render() {
    const {
      prefixCls,
      visible,
      spinning,
      current,
      total
    } = this.props;
    console.log(spinning);
    const classSet = classNames({
      [`${prefixCls}`]: true,
      'showed': visible === true,
      'hidden': visible === false,
    });

    return (
      <div className={classSet}>
        <Spin spinning={spinning}>
          {this.getResultDOMRender()}
        </Spin>
      </div>
    );
  }
}

SearchResultBox.defaultProps = {
  prefixCls: 'cs-co-search-result'
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
  foldText: PropTypes.string,
  unfoldText: PropTypes.string,
  onSwitchPage: PropTypes.func,
  onToggleSelection: PropTypes.func
};

export default SearchResultBox;
