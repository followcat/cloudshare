'use strict';
import React, { Component, PropTypes } from 'react';
import VisitingForm from './VisitingForm';
import { Card, Table } from 'antd';

class VisitingSituation extends Component {
  render() {
    const props = this.props;

    return (
      <Card
        title={props.title}
        style={props.style}
      >
        <Table
          columns={props.columns}
          dataSource={props.dataSource}
          size={props.size}
          pagination={props.pagination}
        />
        <VisitingForm {...props}/>
      </Card>
    );
  }
}

VisitingSituation.defaultProps = {
  title: '',
  style: {
    marginBottom: 16,
  },
  columns: [],
  dataSource: [],
  size: 'middle',
};

VisitingSituation.propTypes = {
  title: PropTypes.string,
  style: PropTypes.object,
  columns: PropTypes.array,
  dataSource: PropTypes.array,
  size: PropTypes.string,
  pagination: PropTypes.oneOfType([PropTypes.object, PropTypes.bool]),
};

export default VisitingSituation;
