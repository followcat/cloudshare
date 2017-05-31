'use strict';
import React, { Component, PropTypes } from 'react';

import { Select, Modal } from 'antd';

class ProjectMessage extends Component {
  constructor() {
    super();
    this.getSelectRender = this.getSelectRender.bind(this);
  }

  getSelectRender() {
    const {
      projects,
      project,
      title
    } = this.props;
    
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

    if (project === null) {
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
    } else {
      return selectElement;
    }
  }

  render() {
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
