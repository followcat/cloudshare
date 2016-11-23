'use strict';
import React, { Component, PropTypes } from 'react';
import TablePlus from '../table-plus';

class Company extends Component {
  render() {
    const props = this.props;

    return (
      <TablePlus 
        {...props}
        columns={props.companyColumns}
        elements={props.companyElements}
        isToolbarShowed={true}
        isSearched={false}
        dataSource={props.companyList}
      />
    );
  }
}

Company.defaultProps = {
  companyList: [],
};

Company.propTypes = {
  companyColumns: PropTypes.array,
  companyElements: PropTypes.array,
  companyList: PropTypes.array,
};

export default Company;
