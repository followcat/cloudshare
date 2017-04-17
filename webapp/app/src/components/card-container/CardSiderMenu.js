'use strict';
import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';
import { Menu } from 'antd';
const SubMenu = Menu.SubMenu,
      MenuItem = Menu.Item;

class CardSiderMenu extends Component {
  render() {
    const {
      prefixCls,
      selectedKeys,
      defaultOpenKeys,
      menus
    } = this.props;

    return (
      <div className={prefixCls}>
        <Menu
          selectedKeys={selectedKeys}
          defaultOpenKeys={defaultOpenKeys}
          mode="inline"
          onClick={this.props.onClick}
        >
          {menus.map(menu => {
            return (
              <SubMenu key={menu.subMenu.key} title={menu.subMenu.title}>
                {menu.menuItem.map(item => {
                  return (
                    <MenuItem key={item.key}>
                      <Link to={item.url}>{item.title}</Link>
                    </MenuItem>
                  );
                })}
              </SubMenu>
            );
          })}
        </Menu>
      </div>
    );
  }
}

CardSiderMenu.defaultProps = {
  prefixCls: 'cs-card-sider',
  menus: [],
  selectedKeys: [],
  onClick() {}
};

CardSiderMenu.propTypes = {
  prefixCls: PropTypes.string,
  menus: PropTypes.array,
  selectedKeys: PropTypes.array,
  defaultOpenKeys: PropTypes.array,
  onClick: PropTypes.func
};

export default CardSiderMenu;
