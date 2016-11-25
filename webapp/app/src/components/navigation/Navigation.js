'usd strict';
import React, { Component, PropTypes } from 'react';
import NavigationItem from './NavigationItem';

class Navigation extends Component {
  render() {
    const props = this.props;
    let classes = props.prefixCls;
    if (props.className) {
      classes = `${props.prefixCls} ${props.className}`;
    }

    return (
      <div
        className={classes}
        style={props.style}
      >
        {props.navs.map((item, index) => {
          return (
            <NavigationItem
              key={item.key || index}
              render={item.render}
            />
          );
        })}
      </div>
    );
  }
}

Navigation.defaultProps = {
  prefixCls: 'cs-nav',
  className: '',
  navs: [],
};

Navigation.propTypes = {
  prefixCls: PropTypes.string,
  className: PropTypes.string,
  style: PropTypes.object,
  navs: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    render: PropTypes.func,
  }))
};

export default Navigation;
