'use strict';
import React, { Component } from 'react';
import Viewport from '../components/viewport';
import Header from '../components/header';
import CommonNavigation from './CommonNavigation';
import Container from '../components/container';
import ResumeContent from '../components/common/ResumeContent';
import { URL } from '../config/url';
import { getEnglishResume } from '../request/resume';
import './upload-preview.less'

export default class UploadPreview extends Component {
  constructor() {
    super();
    this.state = {
      html: '',
    };
    this.getEnglishResumeData = this.getEnglishResumeData.bind(this);
  }

  componentDidMount() {
    this.getEnglishResumeData();
  }

  getEnglishResumeData() {
    getEnglishResume((json) => {
      if (json.code === 200) {
        this.setState({
          html: json.data.markdown,
        });
      }
    });
  }

  render() {
    return (
      <Viewport>
        <Header
          fixed={false}
          logoLink={URL.getSearchURL()}
        >
          <CommonNavigation />
        </Header>
        <Container>
          <ResumeContent html={this.state.html} />
        </Container>
      </Viewport>
    );
  }
}