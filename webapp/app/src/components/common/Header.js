'use strict';
import React, { Component } from 'react';

import { Icon } from 'antd';

import HeaderPerson from './HeaderPerson';

import LogoImg from '../../image/logo.png';

import StorageUtil from '../../utils/storage';
import './header.less';

export default class Header extends Component {

  render() {
    return (
      <div className="cs-layout-top">
        <div className="cs-layout-herader">
          <div className="cs-layout-wrapper">
            <div className="cs-layout-logo">
              <a href="/search">
                <img src={LogoImg} alt="Logo" />
              </a>
            </div>
            <div className="cs-layout-nav">
              <div className="cs-layout-item">
                <p>{StorageUtil.get('_pj')}</p>
              </div>
              <div className="cs-layout-item">
                <HeaderPerson />
              </div>
              <div className="cs-layout-item">
                <a href="/upload" target="_blank">Uploader</a>
              </div>
              <div className="cs-layout-item">
                <a href="/listjd" target="_blank">JD List</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}