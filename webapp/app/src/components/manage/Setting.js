'use strict';
import React, { Component, PropTypes } from 'react';
import ChangePassword from '../change-password';

class Setting extends Component {
  render() {
    const props = this.props;

    return (
      <div
        className={props.className}
        style={props.style}
      >
        <ChangePassword onSubmit={props.onSubmit} />
      </div>
    );
  }
}

Setting.defaultProps = {
  style: {},
  onSubmit() {},
};

Setting.propTypes = {
  style: PropTypes.object,
  className: PropTypes.string,
  onSubmit: PropTypes.func,
};

export default Setting;
