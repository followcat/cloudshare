'use strict';
import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';

import { Menu } from 'antd';

const MenuItem = Menu.Item;

class SubheadNav extends Component {
  render() {
    const props = this.props;

    return (
      <div className={`${props.prefixCls}`}>
        <div className={`${props.prefixCls}-wrap`}>
          <Menu
            selectedKeys={props.selectedKeys}
            mode="horizontal"
            onClick={props.onClick}
            style={props.style}
          >
            {props.menus.map(item => {
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
