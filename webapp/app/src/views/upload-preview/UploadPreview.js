'use strict';
import React, { Component } from 'react';

import Container from 'components/container';
import ResumeContent from 'components/resume-content';

import { getEnglishResume } from 'request/resume';

class UploadPreview extends Component {
  constructor() {
    super();
    this.state = {
      html: ''
    };
    this.getDataSource = this.getDataSource.bind(this);
  }

  componentDidMount() {
    this.getDataSource();
  }

  getDataSource() {
    console.log(getEnglishResume);
    getEnglishResume(json => {
      if (json.code === 200) {
        this.setState({
          html: json.data.markdown
        });
      }
    });
  }

  render() {
    const { html } = this.state;

    return (
      <Container>
        <ResumeContent html={html} />
      </Container>
    );
  }
}

export default UploadPreview;
