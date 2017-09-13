'use strict';
import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';

import { Menu } from 'antd';

import { isMemberAdmin } from 'request/member';
import  websiteText  from 'config/website-text'

const MenuItem = Menu.Item;
const MenuItemGroup = Menu.ItemGroup;
const SubMenu = Menu.SubMenu;
const language = websiteText.zhCN;

class SubheadNav extends Component {
  constructor() {
    super();
    this.state = {
      show :false,
    };
  }

  componentWillMount() {
      isMemberAdmin((json) => {
      if (json.result === true) {
        this.setState({
          show: true,
        });
      }
      });
  }

  render() {
    const {
      prefixCls,
      selectedKeys,
      style,
      menus
    } = this.props;

    return (
      <div className={prefixCls}>
        <div className={`${prefixCls}-wrap`}>
          <Menu
            selectedKeys={selectedKeys}
            defaultopenKeys={selectedKeys}
            mode="horizontal"
            onClick={this.props.onClick}
          >
          { this.state.show ?
          <MenuItem key="invite">
              <Link to='/pm/listcustomer'>{language.MEMBER_MANAGEMENT}</Link>
          </MenuItem>
          :null
          }
          { this.state.show ?
          <MenuItem key="project">
            <Link to='/pm/projectlist'>{language.PROJECT_MANAGEMENT}</Link>
          </MenuItem>
          : null
          }
            {menus.map(item => {
              return (
                <MenuItem key={item.key}>
                  <Link to={item.url}>{item.title}</Link>
                </MenuItem>
              );
            })}
          </Menu>
        </div>
      </div>
    );
  }
}

SubheadNav.defaultProps = {
  prefixCls: 'cs-layout-subhead',
  selectedKeys: [],
  menus: [],
  onClick() {}
};

SubheadNav.propTypes = {
  prefixCls: PropTypes.string,
  selectedKeys: PropTypes.array,
  menus: PropTypes.array,
  style: PropTypes.object,
  onClick: PropTypes.func
};

export default SubheadNav;
