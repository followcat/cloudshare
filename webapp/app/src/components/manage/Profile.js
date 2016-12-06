'use strict';
import React, { Component,PropTypes } from 'react';
import { Dropdown, Icon } from 'antd';

class Profile extends Component {
  render() {
    const props = this.props;

    return (
      <Dropdown
        overlay={props.dropdownMenu}
        trigger={props.trigger}
      >
        <a className="ant-dropdown-link" href="#">
          <Icon type={props.iconType} />{props.text} <Icon type="down" />
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
  trigger: PropTypes.arrayOf(PropTypes.string),
  iconType: PropTypes.string,
  text: PropTypes.string,
};

export default Profile;
