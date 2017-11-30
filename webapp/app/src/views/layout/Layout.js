'use strict';
import React, { Component, PropTypes } from 'react';

import LayoutHeader from './LayoutHeader';
import LayoutContainer from './LayoutContainer';
import AccountLayoutHeader from './AccountLayoutHeader';

import { isMember } from 'request/member';

class Layout extends Component {
  constructor() {
    super();
    this.state = {
      ismember: (sessionStorage.getItem("ismember") === "true"),
    };
  }

  // async componentWillMount() {
  //   await isMember((json) => {
  //     if (json.result === true) {
  //       this.setState({
  //         ismember: true,
  //       });
  //       global.ismember = true
  //     }else{
  //       this.setState({
  //         ismember: false,
  //       });
  //       global.ismember = false
  //     }
  //   });
  // }

  componentDidMount() {
    if( sessionStorage.getItem("ismember") == null && global.ismember) {
      this.setState({
        ismember: true
      })
    }
  }

  render() {
    return (
      <div className="cs-layout">
      { this.state.ismember || global.ismember? 
        <LayoutHeader />
        :
        <AccountLayoutHeader />
      }
        <LayoutContainer>
          {this.props.children}
        </LayoutContainer>
      </div>
      
    );
  }
}

Layout.propTypes = {
  children: PropTypes.oneOfType([PropTypes.element, PropTypes.arrayOf(PropTypes.element)])
};

export default Layout;
