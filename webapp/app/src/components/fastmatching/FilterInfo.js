'use strict';
import React, { Component, PropTypes } from 'react';

export default class FilterInfo extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const style = this.props.visible ? { display: 'block' } : { display: 'none' };
    return (
      <div style={style}>
        <p>About {this.props.total} results.</p>
      </div>
    );
  }
}