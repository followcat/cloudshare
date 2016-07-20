import React from 'react';
import HeaderComponent from './components/HeaderComponent';


export default class UserManageView extends React.Component {

  constructor(props) {
    super(props);

  }

  render() {
    return (
      <HeaderComponent {...this.props} />
    );
  }
}
