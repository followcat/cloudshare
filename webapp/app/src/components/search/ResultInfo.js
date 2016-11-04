'use strict';
import React, { Component } from 'react';

import Position from '../common/analyse/Position';
import Competency from '../common/analyse/Competency';
import Experience from '../common/analyse/Experience';

export default class ResultInfo extends Component {

  render() {
    const btnStyle = {
      display: 'inline-block',
      marginLeft: 4,
    };

    return (
      <div className="top-container">
        <div className="left-wrap">
          <p>About {this.props.total} results</p>
          <p>Search keyword: <strong>{this.props.keyword}</strong></p>
        </div>
        <div className="right-wrap">
          <div><p style={{ fontWeight: 'bold' }}>Analyse:</p></div>
          <Position 
            style={btnStyle}
            keyword={this.props.keyword}
          />
          <Competency
            style={btnStyle}
            dataSource={this.props.dataSource}
          />
          <Experience
            style={btnStyle}
            dataSource={this.props.dataSource}
          />
        </div>
      </div>
    );
  }
}