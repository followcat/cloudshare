'use strict';
import React, { Component, PropTypes } from 'react';
import LogoImg from '../../image/logo.png';

class Header extends Component {
  constructor() {
    super();
    this.getLogoStyle = this.getLogoStyle.bind(this);
  }

  getLogoStyle() {
    return this.props.logoMode === 'center' ? { margin: '0 auto' } : null;
  }

  render() {
    const props = this.props;

    let classes = props.prefixCls;
    if (props.fixed) {
      classes = `${classes} ${props.prefixCls}-fixed`;
    }

    return (
      <div className={classes}>
        <div className={`${props.prefixCls}-container`}>
          <div className={`${props.prefixCls}-logo`} style={this.getLogoStyle()}>
            <img src={LogoImg} alt="logo" />
          </div>
          {props.children}
        </div>
      </div>
    );
  }
}

Header.defaultProps = {
  fixed: false,
  prefixCls: 'cs-header',
  logoMode: 'left',
};

Header.propTypes = {
  fixed: PropTypes.bool,
  prefixCls: PropTypes.string,
  logoMode: PropTypes.string,
};

export default Header;
