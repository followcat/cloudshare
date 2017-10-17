'use strict';
import React, { Component, PropTypes } from 'react';

import echarts from 'echarts';

class Charts extends Component {
  constructor() {
    super();
  }

  componentDidMount() {
    this.init();
    this.setOption();
  }

  componentDidUpdate() {
    // this.setOption();
  }

  componentUnMount() {
    this.dispose();
  }

  init() {
    this.charts = echarts.init(this.refs.charts);
    this.charts.showLoading();
    this.setOption();
  }

  setOption() {
    const { option } = this.props;

    if(option) {
      this.charts.setOption(option);
      this.charts.hideLoading();
      this.props.getLoading(false);
    }
  }

  dispose() {
    this.charts.dispose();
  }

  render() {
    return (
      <div ref="charts" style={this.props.style}></div>
    );
  }
}

Charts.propTypes = {
  option: PropTypes.object,
  style: PropTypes.object
};

export default Charts;
