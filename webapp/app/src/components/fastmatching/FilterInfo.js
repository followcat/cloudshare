'use strict';
import React, { Component, PropTypes } from 'react';

export default class FilterInfo extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <p>About {this.props.total} results.</p>
      </div>
    );
  }
}