'use strict';
import React, { Component, PropTypes } from 'react';
import TablePlus from '../table-plus';

class UserList extends Component {
  render() {
    return (
      <TablePlus {...this.props} />
    );
  }
}

export default UserList;
