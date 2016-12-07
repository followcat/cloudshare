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
      >
        {this.props.menus.map((v, i) => {
          return (
            <MenuItem key={i}>
              <a href={v.url}>{v.text}</a>
            </MenuItem>
          );
        })}
      </Menu>
    );
  }
}

Navigation.defaultProps = {
  menus: []
};

Navigation.propTypes = {
  menus: PropTypes.arrayOf(PropTypes.shape({
    url: PropTypes.string,
    text: PropTypes.string,
  }))
};

export default Navigation;
