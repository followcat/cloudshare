'use strict';
import React, { Component } from 'react';

import TablePlus from 'components/table-plus';
import ButtonWithModal from 'components/button-with-modal';
import ProjectListForm from 'components/project-list';

import {   message,Form,Table, Input,Button, Popconfirm } from 'antd';

import findIndex from 'lodash/findIndex';

import { getProject,addProject } from 'request/project';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;

import { URL } from 'config/url'

class ProjectList extends Component {
	constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      visible: false,
      value: '',
      projectName: '',
    };
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleSubmit   = this.handleSubmit.bind(this);
    this.handleOkClick = this.handleOkClick.bind(this);
    this.getProjectName = this.getProjectName.bind(this);
  }

  getProjectData() {
    getProject((json) => {
      if (json.code === 200) {
		var jsontest = [];
		var fin = [];
		json.data.map((item,index) => { return jsontest.push('{"key"'+':"'+index+'",'+'projectname'+':"'+item+'"}') });
		jsontest.map((item,index) => { return fin.push(eval('(' + item + ')')) });
		this.setState({
          projects: fin,
        });
      }
    });
  }

  getProjectName(childname){
    this.setState({ projectName: childname });
  }

  handleButtonClick() {
    this.setState({
      visible: true
    });
  }

  handleOkClick(){
     this.handleSubmit();
  }

  handleSubmit (feildValue) {
    addProject({
      projectname: this.state.projectName || feildValue.projectname,
    }, (json) => {
      if  (json.code === 200) {
        this.setState({
      visible: false
    });
      message.success(language.ADD_SUCCESS_MSG);
      } else {
        message.error(language.ADD_FAIL_MSG);
      }
    })
  }

  handleCancelClick() {
    this.setState({
      visible: false
    });
  }

  getElements() {
    const elements = [{
      col: {
        span: 4
      },
      render: (
        <ButtonWithModal
          buttonStyle={{ marginLeft: 8 }}
          buttonType="primary"
          buttonText="创建新的项目"
          visible={this.state.visible}
          modalTitle="创建新的项目"
          modalOkText="提交"
          modalCancelText="取消"
          onButtonClick={this.handleButtonClick}
          onModalOk={this.handleOkClick}
          onModalCancel={this.handleCancelClick}
        >
        <ProjectListForm
              getProjectName={this.getProjectName}
              onChange={this.handleFormChange}
              onSubmit={this.handleSubmit}
        />
        </ButtonWithModal>
      )
    }];

    return elements;
  }


  componentDidMount() {
    this.getProjectData();
    }

  render() {
  	const columns = [{
  		title: 'projectName',
  		dataIndex: 'projectname',
  		render: text => <a href="#">{text}</a>,
		}, {
 		 title: 'action',
  		className: 'action',
  		dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.projects.length > 1 ?
          (
            <Popconfirm title="Sure to delete?" >
              <a href="#">change</a>
            </Popconfirm>
          ) : null
        );
      },
		}];

  	const data = this.state.projects;
    return (
    <div className="cs-project-list">
      <TablePlus
          isToolbarShowed={true}
          isSearched={true}
          elements={this.getElements()}
          columns={columns}
          dataSource={this.state.projects}
          loading={this.state.loading}
      />
    </div>
    );
  }
}
export default ProjectList;