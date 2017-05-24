'use strict';
import React, { Component, PropTypes } from 'react';

import { Card } from 'antd';

class ResumeSimilar extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Card
        title="Similar"
        className="mg-t-8"
      >
        <div className="similar">
          {this.props.dataSource.map((item, index) => {
            return (
              <div key={index} className="similar-item">
                <a href={`/resume/${item.id}`}>
                  {item.yaml_info.name ? item.yaml_info.name : item.id}
                  {item.yaml_info.position ? ' | ' + item.yaml_info.position : ''}
                  {item.yaml_info.age ? ' | ' + item.yaml_info.age : ''}
                  {item.yaml_info.gender ? ' | ' + item.yaml_info.gender : ''}
                  {item.yaml_info.education ? ' | ' + item.yaml_info.education : ''}
                </a>
              </div>
            );
          })}
        </div>
      </Card>
    );
  }
}

ResumeSimilar.propTypes = {
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string,
      yaml_info: PropTypes.shape({
        name: PropTypes.string,
        position: PropTypes.string,
        age: PropTypes.string,
        gender: PropTypes.string,
        education: PropTypes.string,
      }),
    })
  ),
};

export default ResumeSimilar;
