'use strict';
import React, { Component } from 'react';

import { Icon, Input, Button } from 'antd';

import HeaderPerson from './HeaderPerson';
import SearchInput from './SearchInput';

import LogoImg from '../../image/logo.png';

import StorageUtil from '../../utils/storage';
import './header.less';

export default class Header extends Component {

  render() {
    const searchDOM = this.props.search ? (
                      <div className="cs-layout-search">
                        <SearchInput
                          value={this.props.search}
                          onSearch={this.props.onSearch}
                          placeholder="Input search text"
                          style={{ width: 200 }}
                        />
                      </div> ) : '';
    const fixCls = this.props.fixed ? 'cs-layout-top fixed' : 'cs-layout-top';
    return (
      <div className={fixCls}>
        <div className="cs-layout-header">
          <div className="cs-layout-wrapper">
            <div className="cs-layout-logo">
              <a href="/search">
                <img src={LogoImg} alt="Logo" />
              </a>
            </div>
            {searchDOM}
            <div className="cs-layout-nav">
              <div className="cs-layout-item">
                <p>{StorageUtil.get('_pj')}</p>
              </div>
              <div className="cs-layout-item">
                <HeaderPerson />
              </div>
              <div className="cs-layout-item">
                <a href="/uploader" target="_blank">Uploader</a>
              </div>
              <div className="cs-layout-item">
                <a href="/pm" target="_blank">JD List</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}