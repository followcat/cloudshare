'use strict';
import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';

import { Menu } from 'antd';

const MenuItem = Menu.Item;
const MenuItemGroup = Menu.ItemGroup;
const SubMenu = Menu.SubMenu;

class SubheadNav extends Component {
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
            mode="inline"
            onClick={this.props.onClick}
          >
          <MenuItem key="project">
            <Link to='/pm/projectlist'>project</Link>
          </MenuItem>
          <SubMenu key="service" title="service">
            {menus.map(item => {
              return (
                <MenuItem key={item.key}>
                  <Link to={item.url}>{item.title}</Link>
                </MenuItem>
              );
            })}
            </SubMenu>
            <MenuItem key="invite" title="invite">
              <Link to='/pm/invite'>invite</Link>
            </MenuItem>
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
