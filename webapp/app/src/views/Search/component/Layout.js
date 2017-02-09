'use strict';
import React, { Component, PropTypes } from 'react';

import LayoutHeader from '../../common/LayoutHeader';
import LayoutContainer from '../../common/LayoutContainer';

class Layout extends Component {
  render() {
    return (
      <div>
        <LayoutHeader />
        <LayoutContainer>
          {this.props.children}
        </LayoutContainer>
      </div>
      
    );
  }
}

Layout.propTypes = {
  children: PropTypes.element
};

export default Layout;
