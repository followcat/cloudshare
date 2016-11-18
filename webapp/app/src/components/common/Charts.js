'use strict';
import React, { Component, PropTypes } from 'react';

import echarts from 'echarts';

export default class Charts extends Component {

  constructor(props) {
    super(props);
  }

  init() {
    this.charts = echarts.init(this.refs.charts);
    this.charts.showLoading();
    this.setOption();
  }

  setOption() {
    // this.charts.showLoading();
    if(this.props.option) {
      // this.charts.showLoading();
      this.charts.setOption(this.props.option);
      this.charts.hideLoading();
    }
  }

  dispose() {
    this.charts.dispose();
  }

  componentDidMount() {
    this.init();
  }

  componentDidUpdate() {
    this.setOption();
  }

  componentUnMount() {
    this.dispose();
  }

  render() {
    return (
      <div ref="charts" style={this.props.style}></div>
    );
  }
}