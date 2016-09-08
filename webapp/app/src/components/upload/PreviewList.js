'use strict';
import React, { Component } from 'react';

import Preview from './Preview';

export default class PreviewList extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        {this.props.previewList.map((previewItem) => {
          return (
            <Preview />
          );
        })}
      </div>
    );
  }
}