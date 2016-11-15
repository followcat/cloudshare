'use strict';
import React, { Component } from 'react';

import './home.less';

class Home extends Component {
  render() {
    return (
      <div className="viewport">
        {this.props.children}
      </div>
    );
  }
}

export default Home;
