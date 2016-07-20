import React from 'react';
import styles from './style.css';

import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import PersonIcon from 'material-ui/svg-icons/social/person';

import LogoComponent from '../../common/logo/LogoComponent';

export default class HeaderComponent extends React.Component {

  constructor(props) {
    super(props);

  }

  render() {
    return (
      <div className={ styles.header }>
        <div className={ styles.headerWrap }>
          <LogoComponent {...this.props}/>
        </div>
      </div>
    );
  }
}
