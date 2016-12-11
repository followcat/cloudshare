'use strict';
import React, { Component, PropTypes } from 'react';
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
          mode="inline"
        >
          {props.menus.map((menu, i) => {
            return (
              <SubMenu key={i} title={menu.subMenuTitle}>
                {menu.menuItems.map(item => {
                  return <MenuItem key={item}>{item}</MenuItem>
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
  menus: PropTypes.arrayOf(PropTypes.shape({
    subMenuTitle: PropTypes.string,
    MenuItem: PropTypes.array,
  })),
  selectedKeys: PropTypes.array,
};

export default CardSiderMenu;
