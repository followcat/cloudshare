'use strict';
import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';
import { Menu } from 'antd';
const SubMenu = Menu.SubMenu,
      MenuItem = Menu.Item;

class CardSiderMenu extends Component {
  render() {
    const props = this.props;

    return (
      <div className="cs-card-sider">
        <Menu
          selectedKeys={props.selectedKeys}
          defaultOpenKeys={props.defaultOpenKeys}
          mode="inline"
          onClick={props.onClick}
        >
          {props.menus.map(menu => {
            return (
              <SubMenu key={menu.subMenu.key} title={menu.subMenu.title}>
                {menu.menuItem.map(item => {
                  return (
                    <MenuItem key={item.key}>
                      <Link to={item.url}>{item.title}</Link>
                    </MenuItem>
                  )
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
  menus: [],
  selectedKeys: [],
};

CardSiderMenu.propTypes = {
  menus: PropTypes.array,
  selectedKeys: PropTypes.array,
};

export default CardSiderMenu;
