'use strict';
import React, { Component } from 'react';

import moment from 'moment';

import { message, Card, Button,Icon,Form,Input, Table } from 'antd';

import CreateNewJobDescription from './CreateNewJobDescription';
import ShowCard from 'components/show-card';
import TablePlus from 'components/table-plus';
import SearchResultBox from 'components/search-result-box';

import Operation from './Operation';

import StorageUtil from 'utils/storage';

import { API } from 'API';

import { getLSIAllSIMS, getIndustry } from 'request/classify';
import { becomeMember } from 'request/member';
import { getCustomerList } from 'request/company';
import { createJobDescription,   getJobDescription } from 'request/jobdescription';
import { getFastMatching } from 'request/fastmatching';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

const FormItem = Form.Item;

class AddPosition extends Component {
  constructor() {
    super();
    this.state = {
      dataSource: [],
      filterDataSource: [],
      customerDataSource: [],
      newjd: [],
      statusValue: 'Opening',
      record: {},
      loading: false,
      editVisible: false,
      editConfirmLoading: false,
      jdVisible: false,
      jdConfirmLoading: false
    };
    this.handleJobDescriptionCreate = this.handleJobDescriptionCreate.bind(this);
    this.getLSIAllSIMSDataSource = this.getLSIAllSIMSDataSource.bind(this);
  }

  componentWillMount () {
    this.getCustomerDataSource();
    this.getFastMatchingByID();
    // this.getJobDescriptionByID();
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

   // 新建职位
  handleJobDescriptionCreate(fieldValues) {
    console.log(fieldValues);
    createJobDescription(fieldValues, (json) => {
      if (json.code === 200) {
        let array = new Array(json.data.info);
        this.setState({
          newjd: array
        });

        message.success(json.message);
      } else {

        message.error(json.message);
      }
    });
  }

    // 根据id获取最新数据
  getJobDescriptionByID(id) {
    let dataSource = this.state.dataSource,
        filterDataSource = this.state.filterDataSource;

    getJobDescription({
      'jd_id': 'be97722a0cff11e6a3e16c3be51cefca'
    }, json => {
      if (json.code === 200) {
        let array = new Array(json.data);
        this.setState({
          newjd: array
        });
      }
    });
  }

  getFastMatchingByID(id) {
    const date = new Date();
    const defFilterData = {date: [moment(date).add(-180, 'days').format('YYYY-MM-DD'),
                                  moment(date).format('YYYY-MM-DD')]};

    let promise = new Promise((resolve, reject) => {
      this.getLSIAllSIMSDataSource(resolve);
    });
    let postAPI = API.LSI_BY_JD_ID_API;

    promise.then((data) => {
        let postData = {
            id: 'be97722a0cff11e6a3e16c3be51cefca',
            uses: data,
            filterdict: defFilterData,
        };
        getFastMatching(postAPI, postData, json => {
          if (json.code === 200) {
            this.setState({
              dataSource: json.data.datas,
              pages: json.data.pages,
              total: json.data.totals
            });
          }
        });
    });
  }

  getLSIAllSIMSDataSource(resolve) {
    getLSIAllSIMS(json => {
      if (json.code === 200) {
        this.setState({
          classify: json.classify,
          projects: json.projects
        });
        resolve(json.projects.concat(json.classify));
      }
    });
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
      key: 'committer',
      width: '10%'
    },{
      title: language.OPERATION,
      key: 'operation',
      width: '10%',
      render: (record) => (
        <Operation 
          record={record}
          onEdit={this.handleEditClick}
        />
      )
    }];

    return (
      <div className="cs-addposition" >
      <ShowCard>
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
          onCreate={this.handleJobDescriptionCreate}
        />
        <Table dataSource={this.state.newjd} columns={columns} />
        <SearchResultBox
          type="match"
          visible={true}
          spinning={false}
          current={0}
          total={this.state.total}
          dataSource={this.state.dataSource}
          educationExperienceText="教育经历"
          workExperienceText="工作经历"
          foldText="展开"
          unfoldText="收起"
          onToggleSelection={null}
        />
      </ShowCard>
      </div>
    );
  }
}

export default AddPosition;