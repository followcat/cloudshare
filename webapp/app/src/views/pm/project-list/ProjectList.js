'use strict';
import React, { Component } from 'react';

import TablePlus from 'components/table-plus';

import { message,Table } from 'antd';

import findIndex from 'lodash/findIndex';

import {
  getJobDescriptionList,
  getJobDescription,
  updateJobDescription,
  createJobDescription
} from 'request/jobdescription';
import { getProject } from 'request/project';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class ProjectList extends Component {
	constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: []
    };
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
		}];

  	const data = this.state.projects;
    return (
    <div className="cs-project-list">
		<Table
     columns={columns}
     dataSource={this.state.projects}
      title={() => 'ProjectList'}
    />
    </div>
    );
  }
}
export default ProjectList;