'use strict';
import React, { Component, PropTypes } from 'react';
import LayoutHeader from './LayoutHeader';
import Navigation from './Navigation';
import ProjectMessage from './ProjectMessage';
import Profile from './Profile';
import { Dropdown, Icon } from 'antd';

class Header extends Component {
  render() {
    const props = this.props;

    return (
      <LayoutHeader logoImg={props.logoImg}>
        <Navigation
          menus={props.navMenus}
          selectedKeys={props.selectedKeys}
        />
        <ProjectMessage project={props.project} />
        <Profile>
          <Dropdown overlay={props.profileMenu}>
            <a className="cs-dropdown-link" href="#">
              {props.profileText} <Icon type="down" />
            </a>
          </Dropdown>
        </Profile>
      </LayoutHeader>
    );
  }
}

Header.defaultProps = {
  logoImg: '',
  navMenus: [],
  profileMenu: null,
  profileText: '',
};

Header.propTypes = {
  logoImg: PropTypes.string,
  navMenus: PropTypes.arrayOf(PropTypes.shape({
    url: PropTypes.string,
    text: PropTypes.string,
  })),
  profileText: PropTypes.string,
  profileMenu: PropTypes.element,
};

export default Header;
