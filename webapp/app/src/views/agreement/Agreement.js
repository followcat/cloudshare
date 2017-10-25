'use strict';
import React, { Component } from 'react';
import { browserHistory, Link } from 'react-router';

import Header from 'components/header';

class Agreement extends Component {
  constructor() {
    super();
    this.state = {
    };
    this. createMarkup = this. createMarkup.bind(this);
  }

  createMarkup() {
    return {__html: require('./agreement.html')};
  }

  componentDidMount() {

  }

  render() {
    return (
      <div className="cs-agreement">
        <Header logoMode="center" />
        <div className='cs-agreement-wrap'>
          <div className='cs-agreement-container' 
          dangerouslySetInnerHTML={this.createMarkup()} />;
          </div>
      </div>
    );
  }
}

export default Agreement;
