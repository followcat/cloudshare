'use strict';
import React, { Component } from 'react';

import TablePlus from '../../../components/table-plus';
import EditJobDescriptionForm from './EditJobDescriptionForm';
import CreateNewJobDescription from './CreateNewJobDescription';
import Status from './Status';

import { message } from 'antd';

import {
  getJobDescriptionList,
  updateJobDescription,
  createJobDescription
} from '../../../request/jobdescription';
import { getCustomerList } from '../../../request/company';
import { URL } from '../../../config/url';

import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;

class JobDescription extends Component {
  constructor() {
    super();
    this.state = {
      dataSource: [],
      filterDataSource: [],
      customerDataSource: [],
      statusValue: 'Opening',
      record: {},
      loading: false,
      editVisible: false,
      editConfirmLoading: false,
      jdVisible: false,
      jdConfirmLoading: false
    };
    this.handleEditClick = this.handleEditClick.bind(this);
    this.handleEditFormCancel = this.handleEditFormCancel.bind(this);
    this.handleEditJobDescriptionSubmit = this.handleEditJobDescriptionSubmit.bind(this);
    this.handleNewJDBtnClick = this.handleNewJDBtnClick.bind(this);
    this.handleJDModalCancel = this.handleJDModalCancel.bind(this);
    this.handleJobDescriptionCreate = this.handleJobDescriptionCreate.bind(this);
    this.handleStatusChange = this.handleStatusChange.bind(this);
    this.getjobDescriptionDataSource = this.getjobDescriptionDataSource.bind(this);
    this.getExpandedRowRender = this.getExpandedRowRender.bind(this);
    this.getJobDescriptionElements = this.getJobDescriptionElements.bind(this);
  }

  componentDidMount() {
    this.getjobDescriptionDataSource();
    this.getCustomerDataSource();
  }

  handleEditClick(record) {
    this.setState({
      record: record,
      editVisible: true
    });
  }

  // 编辑职位Modal关闭事件
  handleEditFormCancel() {
    this.setState({
      editVisible: false
    });
  }

  /*
   * 提交修改职位信息
   * @param  {object} fieldValues 表单数据
   * @return {void}
   */
  handleEditJobDescriptionSubmit(fieldValues) {
    this.setState({
      editConfirmLoading: true
    });

    const params = {
      jd_id: fieldValues.id,
      description: fieldValues.description,
      status: fieldValues.status
    };

    updateJobDescription(params, (json) => {
      if (json.code === 200) {
        this.getjobDescriptionDataSource();
        this.setState({
          editConfirmLoading: false,
          editVisible: false
        });
        message.success(json.message);
      } else {
        this.setState({
          editConfirmLoading: false
        });
        message.error(json.message);
      }
    });
  }

  // 新建职位按钮事件, 打开Modal
  handleNewJDBtnClick() {
    this.setState({
      jdVisible: true
    });
  }

  // 新建职位Modal关闭事件, 关闭Modal
  handleJDModalCancel() {
    this.setState({
      jdVisible: false
    });
  }

  handleJobDescriptionCreate(fieldValues) {
    this.setState({
      jdConfirmLoading: true
    });

    createJobDescription(fieldValues, (json) => {
      if (json.code === 200) {
        this.getjobDescriptionDataSource();
        this.setState({
          jdVisible: false,
          jdConfirmLoading: false
        });
        message.success(json.message);
      } else {
        this.setState({
          jdConfirmLoading: false
        });
        message.error(json.message);
      }
    });
  }

  handleStatusChange(value) {
    const dataSource = this.state.dataSource;
    let filterDataSource = [];

    if (value) {
      filterDataSource = dataSource.filter(v => {
        return v.status === value;
      });
    }

    this.setState({
      statusValue: value,
      filterDataSource: filterDataSource
    });
  }

  // 获取所有JD列表
  getjobDescriptionDataSource() {
    const statusValue = this.state.statusValue;
    
    this.setState({
      loading: true
    });
    
    getJobDescriptionList((json) => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          filterDataSource: json.data.filter(item => item.status === statusValue),
          loading: false
        });
      }
    });
  }

  // 获取客户公司列表
  getCustomerDataSource() {
    getCustomerList((json) => {
      if (json.code === 200) {
        this.setState({
          customerDataSource: json.data
        });
      }
    });
  }

  // 获取渲染扩展JD展开行
  getExpandedRowRender(record) {
    return record.description.split('\n').map((item, index) => {
      return <p key={index}>{item}</p>;
    });
  }

  // 获取职位描述组件toolbar所要渲染组件
  getJobDescriptionElements() {
    const statusList = [{
      text: language.ALL,
      value: ''
    }, {
      text: language.OPENING,
      value: 'Opening'
    }, {
      text: language.CLOSED,
      value: 'Closed'
    }];

    const elements = [{
      col: {
        span: 2,
      },
      render: (
        <CreateNewJobDescription
          buttonStyle={{ marginLeft: 10 }}
          buttonType="primary"
          buttonText={language.CREATION}
          modalTitle={language.JOB_DESCRIPTION_CREATION}
          modalOkText={language.SUBMIT}
          modalCancelText={language.CANCEL}
          companyList={this.state.customerDataSource}
          confirmLoading={this.state.jdConfirmLoading}
          visible={this.state.jdVisible}
          onButtonClick={this.handleNewJDBtnClick}
          onModalCancel={this.handleJDModalCancel}
          onCreate={this.handleJobDescriptionCreate}
        />
      )
    }, {
      col: {
        span: 8,
      },
      render: (
        <Status
          statusLabel={language.CURRENT_STATUS}
          dataSource={statusList}
          width={120}
          defaultValue={this.state.statusValue}
          onChange={this.handleStatusChange}
        />
      )
    }];

    return elements;
  }

  render() {
    const columns = [{
      title: language.COMPANY_NAME,
      dataIndex: 'company_name',
      key: 'company_name',
      width: '30%'
    }, {
      title: language.POSITION,
      dataIndex: 'name',
      key: 'name',
      width: '40%'
    }, {
      title: language.CREATOR,
      dataIndex: 'committer',
      key: 'creator',
      width: '10%'
    }, {
      title: language.CURRENT_STATUS,
      dataIndex: 'status',
      key: 'status',
      width: '10%',
      render: (text) => {
        return text === 'Opening' ? 
            <span style={{ color: 'green' }}>{language.OPENING}</span> :
            <span style={{ color: 'red' }}>{language.CLOSED}</span>;
      }
    }, {
      title: language.OPERATION,
      key: 'operation',
      width: '10%',
      render: (record) => (
        <ul>
          <li><a href={URL.getFastMatching(record.id)}>{language.MATCH_ACTION}</a></li>
          <li><a href="javascript: void(0);" onClick={() => this.handleEditClick(record)}>{language.EDIT}</a></li>
        </ul>
      )
    }];

    const state = this.state;

    return (
      <div>
        <TablePlus
          isToolbarShowed={true}
          isSearched={true}
          loading={this.state.loading}
          elements={this.getJobDescriptionElements()}
          columns={columns}
          rowKey={record => record.id}
          expandedRowRender={record => this.getExpandedRowRender(record)}
          dataSource={state.filterDataSource.length > 0 ? state.filterDataSource : state.dataSource}
        />
        <EditJobDescriptionForm
          visible={state.editVisible}
          confirmLoading={state.editConfirmLoading}
          onSubmit={this.handleEditJobDescriptionSubmit}
          onCancel={this.handleEditFormCancel}
          record={this.state.record}
          customerDataSource={this.state.customerDataSource}
        />
      </div>
    );
  }
}

export default JobDescription;
