'use strict';
import React, { Component } from 'react';

import { Icon } from 'antd';

import HeaderPerson from './HeaderPerson';

import LogoImg from '../../image/logo.png';

export default class Header extends Component {

  render() {
    return (
      <div>
        <div className="cs-layout-top">
          <div className="cs-layout-herader">
            <div className="cs-layout-wrapper">
              <div className="cs-layout-logo">
                <a href="/search">
                  <img src={LogoImg} alt="Logo" />
                </a>
              </div>
              <div className="cs-layout-person">
                <HeaderPerson />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}