'use strict';
import React, { Component } from 'react';

import LayoutHeader from '../../Header/LayoutHeader';
import { CardContainer, CardSiderMenu, CardContent } from '../../../components/card-container';

import { Menu, Button } from 'antd';

import { getCurrentActive } from '../../../utils/sider-menu-list';
import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;

const SubMenu = Menu.SubMenu,
      MenuItem = Menu.Item;

export default class Layout extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedKey: getCurrentActive(props)
    };
    this.handleCardSiderMenuClick = this.handleCardSiderMenuClick.bind(this);
    this.getTitle = this.getTitle.bind(this);
  }

  handleCardSiderMenuClick(e) {
    this.setState({
      selectedKey: e.key
    });
  }

  getTitle(key, menus) {
    let title = '';

    for (let i = menus.length - 1; i >= 0; i--) {
      for (let j = menus[i].menuItem.length - 1; j >= 0; j--) {
        if (menus[i].menuItem[j].key === key) {
          title = menus[i].menuItem[j].title;
          break;
        }
      }
    }

    return title;
  }

  render() {
    const cardSiderMenus = [{
      subMenu: {
        key: 'jdm',
        title: language.JOB_DESCRIPTION_MANAGEMENT
      },
      menuItem: [{
        key: 'jobdescription',
        title: language.OPEN_JOB_DESCRIPTION,
        url: '/jobdescription'
      }]
    }, {
      subMenu: {
        key: 'cm',
        title: language.CUSTOMER_MANAGEMENT
      },
      menuItem: [{
        key: 'owncustomer',
        title: language.OWN_CUSTOMER_MANAGEMENT,
        url: '/owncustomer'
      }, {
        key: 'developcustomer',
        title: language.DEVELOPMENT_CUSTOMER_MANAGEMENT,
        url: '/developcustomer'
      }]
    }];

    const cardContentTitle = this.getTitle(this.state.selectedKey, cardSiderMenus);

    const defaultOpenKeys = cardSiderMenus.map(v => v.subMenu.key);

    return (
      <LayoutHeader>
        <CardContainer>
          <CardSiderMenu
            menus={cardSiderMenus}
            selectedKeys={[this.state.selectedKey]}
            defaultOpenKeys={defaultOpenKeys}
            onClick={this.handleCardSiderMenuClick}
          />
          <CardContent title={cardContentTitle}>
            {this.props.children}
          </CardContent>
        </CardContainer>
      </LayoutHeader>
    );
  }
}