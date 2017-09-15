'use strict';
import React, { Component, PropTypes } from 'react';

import StorageUtil from 'utils/storage';

import ProjectListForm from 'components/project-list';

import { addProject } from 'request/project';

import { Select, Modal, Button, message } from 'antd';

const defaultproje = null;

class ProjectMessage extends Component {
  constructor() {
    super();
    this.state ={
      projectName: '',
    };
    this.getSelectRender = this.getSelectRender.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit () {
    addProject({
      projectname: this.state.projectName,
    }, (json) => {
      if  (json.result === true) {
        this.setState({
        visible: false,
    });
      message.success(language.ADD_SUCCESS_MSG);
      } else {
        message.error(language.ADD_FAIL_MSG);
      }
    })
  }

  getSelectRender() {
    const {
      isMember,
      projects,
      project,
      title,
    } = this.props;
    let selectElement = (
      <Select
        className="cs-header-project-selection"
        defaultValue={ defaultproje || project || projects[0]}
        onChange={this.props.onChange}
      >
        {projects.map((item) => {
          return (
            <Select.Option key={item} value={item}>{item}</Select.Option>
          );
        })}
      </Select>
    );
    if(isMember !== '' )  {
    if (isMember === true ) {
      if( project !== null ) {
        return selectElement;
      }

      if( project === null && projects.length !== 0 ) {
      return (
        <Modal
          visible={true}
          title={title}
          closable={false}
          footer={<div style={{ padding: 4 }}></div>}
        >
          <label>项目列表: </label>
          {selectElement}
        </Modal>
      );
      }

      if( project === null && projects.length === 0 ) {
      return (
        <Modal
          visible={true}
          title={'新建项目'}
          closable={false}
          footer={[
            <Button key="submit" type="primary" size="large" onClick={this.handleSubmit}>
              确认
            </Button>,
          ]}
        >
        <ProjectListForm
          inputLabel="项目名称"
          getInput={this.getProjectName}
          onChange={this.handleFormChange}
          onSubmit={this.handleSubmit}
        />
        </Modal>
      );
      }
    } else {
      StorageUtil.set('_pj','default');
      this.defaultValue = 'default';
      return selectElement;
       window.location.reload();
      }
    }
  }

  render() {
    this.state =this.props;
    return (
      <div className="cs-header-project">
        {this.getSelectRender()}
      </div>
    );
  }
}

ProjectMessage.defaultProps = {
  title: '选择项目',
};

ProjectMessage.propTypes = {
  title: PropTypes.string,
  okText: PropTypes.string,
  projects: PropTypes.array,
  project: PropTypes.any,
  onChange: PropTypes.func
};

export default ProjectMessage;
