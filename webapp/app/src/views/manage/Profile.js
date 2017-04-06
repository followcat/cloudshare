'use strict';
import React, { Component,PropTypes } from 'react';

import { Dropdown, Icon } from 'antd';

class Profile extends Component {
  render() {
    const { dropdownMenu, trigger, iconType, text } = this.props;

    return (
      <Dropdown
        overlay={dropdownMenu}
        trigger={trigger}
      >
        <a className="ant-dropdown-link" href="#">
          <Icon type={iconType} />{text} <Icon type="down" />
        </a>
      </Dropdown>
    );
  }
}

Profile.defaultProps = {
  trigger: ['click'],
  iconType: '',
  text: '',
};

Profile.propTypes = {
  dropdownMenu: PropTypes.any,
  trigger: PropTypes.arrayOf(PropTypes.string),
  iconType: PropTypes.string,
  text: PropTypes.string,
};

export default Profile;
