'use strict';
import React, { Component, PropTypes } from 'react';
import { Menu } from 'antd';

const MenuItem = Menu.Item; 

class Navigation extends Component {
  render() {
    return (
      <Menu 
        mode="horizontal"
        className="cs-layout-header-nav"
        selectedKeys={this.props.selectedKeys}
      >
        {this.props.menus.map(v => {
          return (
            <MenuItem key={v.url}>
              <a href={v.url}>{v.text}</a>
            </MenuItem>
          );
        })}
      </Menu>
    );
  }
}

Navigation.defaultProps = {
  menus: [],
  defaultSelectedKeys: [],
};

Navigation.propTypes = {
  menus: PropTypes.arrayOf(PropTypes.shape({
    url: PropTypes.string,
    text: PropTypes.string,
  })),
  defaultSelectedKeys: PropTypes.array,
};

export default Navigation;
