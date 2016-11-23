'use strict';
import React, { Component, PropTypes } from 'react';
import './header.less';
import LogoImg from '../../image/logo.png';

class Header extends Component {
  render() {
    const props = this.props;

    let classes = props.prefixCls;
    if (props.fixed) {
      classes += `${props.prefixCls}-fixed`;
    }

    return (
      <div className={classes}>
        <div className={`${props.prefixCls}-container`}>
          <div className={`${props.prefixCls}-logo`}>
            <img src={LogoImg} alt="logo" />
          </div>
          <div className={`${props.prefixCls}-right`}>
            {props.children}
          </div>
        </div>
      </div>
    );
  }
}

Header.defaultProps = {
  fixed: false,
  prefixCls: 'cs-header',
};

Header.propTypes = {
  fixed: PropTypes.bool,
  prefixCls: PropTypes.string,
};

export default Header;
