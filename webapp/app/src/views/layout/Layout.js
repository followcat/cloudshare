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
      ismember: sessionStorage.getItem("ismember"),
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
    if( !this.state.ismember || global.ismember) {
      this.setState({
        ismember: true
      })
    }
  }

  render() {
    console.log(this.state.ismember);
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
