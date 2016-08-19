'use strict';
import React, { Component, PropTypes } from 'react';
import Header from '../components/manage/Header';
import MainWrapper from '../components/manage/MainWrapper';

export default class Manage extends Component {

  render() {
    return (
      <div>
        <div id="viewport">
          <Header />
          <MainWrapper />
        </div>
      </div>
    );
  }
}