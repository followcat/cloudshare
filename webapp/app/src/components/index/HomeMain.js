'use strict';
import React, { Component, PropTypes } from 'react';
import './home-main.less'

class HomeMain extends Component {
  render() {
    const props = this.props;
    let classes = `${props.prefixCls}-center`;

    if (props.className) {
      classes += props.className;
    }

    return(
      <div className={`${props.prefixCls}`}>
        <div className={classes}>
          {props.children}
        </div>
      </div>
    );
  }
}

HomeMain.defaultProps = {
  prefixCls: 'cs-container',
  className: '',
};

HomeMain.propTypes = {
  prefixCls: PropTypes.string,
  className: PropTypes.string,
};

export default HomeMain;
