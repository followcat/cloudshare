'use strict';
import React, { Component, PropTypes } from 'react';

import StorageUtil from 'utils/storage';

import ProjectListForm from 'components/project-list';

import { Select, Modal } from 'antd';

class ProjectMessage extends Component {
  constructor() {
    super();
    this.state;
    this.getSelectRender = this.getSelectRender.bind(this);
  }

  getSelectRender() {
    const {
      isMember,
      projects,
      project,
      title
    } = this.props;
    console.log(isMember );
    let selectElement = (
      <Select
        className="cs-header-project-selection"
        defaultValue={project || projects[0]}
        onChange={this.props.onChange}
      >
        {projects.map((item) => {
          return (
            <Select.Option key={item} value={item}>{item}</Select.Option>
          );
        })}
      </Select>
    );
    if(isMember !== undefined)  {
    if (isMember === true ) {
      if( project !== null ) {
        return selectElement;
      }

      if( project === null && projects !==null ) {
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

      if( project === null && projects ===null ) {
      return (
        <Modal
          visible={true}
          title={title}
          closable={false}
          footer={<div style={{ padding: 4 }}></div>}
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
      console.log(isMember);
      StorageUtil.set('_pj','default');
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
  title: '选择项目'
};

ProjectMessage.propTypes = {
  title: PropTypes.string,
  okText: PropTypes.string,
  projects: PropTypes.array,
  project: PropTypes.any,
  onChange: PropTypes.func
};

export default ProjectMessage;
