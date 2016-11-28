'use strict';
import React, { Component, PropTypes } from 'react';
import TablePlus from '../table-plus';

class JobDescription extends Component {
  render() {
    const props = this.props;
    return (
      <TablePlus 
        {...props}
        columns={props.jobDescriptionColumns}
        elements={props.jobDescriptionElements}
        rowKey={record => record.id}
        isToolbarShowed={true}
        isSearched={true}
        expandedRowRender={(record) => props.getExpandedRowRender(record)}
        dataSource={props.jobDescriptionList}
      />
    );
  }
}

JobDescription.propTypes = {
  jobDescriptionColumns: PropTypes.array,
  jobDescriptionElements: PropTypes.array,
  jobDescriptionList: PropTypes.array,
  getExpandedRowRender: PropTypes.func,
};

export default JobDescription;
