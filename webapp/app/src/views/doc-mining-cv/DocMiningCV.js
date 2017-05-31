'use strict';
import React, { Component } from 'react';

import Resume from 'components/analysis-doc/Resume';

import { getDocMiningCV } from 'request/docmining';

class DocMiningCV extends Component {
  constructor() {
    super();
    this.state = {
      resumeId: '',
      dataSource: {}
    };
    this.getResumeDataSource = this.getResumeDataSource.bind(this);
  }

  componentDidMount() {
    const id = this.props.params.resumeId;

    this.setState({
      resumeId: id
    });

    this.getResumeDataSource(id);
  }

  getResumeDataSource(id) {
    getDocMiningCV({
      id: id
    }, json => {
      if (json.code === 200) {
        const { yaml_info } = json.data;
        this.setState({
          resumeId: id,
          dataSource: yaml_info,
        });
      }
    });
  }

  render() {
    const {
      resumeId,
      dataSource,
    } = this.state;
    return (
      <div>
        <Resume dataSource={ dataSource } />
      </div>
    );
  }
}

export default DocMiningCV;