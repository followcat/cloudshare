'use strict';
import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';
import { Menu } from 'antd';

const MenuItem = Menu.Item;

class SideMenu extends Component {
  render() {
    const props = this.props;

    return (
      <div className={props.prefixCls}>
        <Menu
          mode={props.mode}
          selectedKeys={props.selectedKeys}
          onClick={props.onClick}
        >
          {props.menus.map((item, index) => {
            return (
              <MenuItem key={item.key}>
                <Link to={item.url}>{item.text}</Link>
              </MenuItem>
            );
          })}
        </Menu>
      </div>
    );
  }
}

SideMenu.defaultProps = {
  prefixCls: 'cs-sider-menu',
  mode: 'inline',
  menus: [],
  onClick() {},
};

SideMenu.propTypes = {
  prefixCls: PropTypes.string,
  mode: PropTypes.string,
  selectedKeys: PropTypes.array,
  menus: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    url: PropTypes.string,
    text: PropTypes.string,
  })),
  onClick: PropTypes.func,
};

export default SideMenu;
