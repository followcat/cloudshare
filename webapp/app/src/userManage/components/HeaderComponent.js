import React from 'react';
import styles from './style.css';

import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import PersonIcon from 'material-ui/svg-icons/social/person';

import LogoComponent from '../../common/logo/LogoComponent';


const iconStyles = {
  mediumIcon: {
    width: 30,
    height: 30,
  },
  medium: {
    width: 60,
    height: 60,
    padding: 15,
  }
};

export default class HeaderComponent extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className={ styles.header }>
        <div className={ styles.headerWrap }>
          <LogoComponent {...this.props}/>
          <IconMenu
            iconButtonElement={<IconButton iconStyle={iconStyles.mediumIcon} style={iconStyles.medium}><PersonIcon /></IconButton>}
            anchorOrigin={{horizontal: 'left', vertical: 'top'}}
            targetOrigin={{horizontal: 'left', vertical: 'bottom'}}
            iconStyle={{color: '#fff'}}
            style={{float: 'right'}}
          >
            <MenuItem primaryText="Settings" />
            <MenuItem primaryText="Sign out" />
          </IconMenu>
        </div>
      </div>
    );
  }
}
