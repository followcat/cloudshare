'use strict';
import React, { Component } from 'react';

import moment from 'moment';

import { message, Card, Button,Icon,Form,Input, Table } from 'antd';

import CreateNewJobDescription from './CreateNewJobDescription';
import ShowCard from 'components/show-card';
import TablePlus from 'components/table-plus';
import SearchResultBox from 'components/search-result-box';

import EditJobDescriptionForm from './EditJobDescriptionForm';
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
    // this.getLSIAllSIMSDataSource = this.getLSIAllSIMSDataSource.bind(this);
    this.getFastMatchingByID = this.getFastMatchingByID.bind(this);
    this.getExpandedRowRender = this.getExpandedRowRender.bind(this);
  }

  componentWillMount () {
    this.getCustomerDataSource();
    // this.getFastMatchingByID();
    // this.getJobDescriptionByID();
  }

    // 获取客户公司列表
  getCustomerDataSource() {
    getCustomerList({
      current_page: 1,
      page_size: 999,
    },(json) => {
      if (json.code === 200) {
        this.setState({
          customerDataSource: json.data
        });
      }
    });
  }

   // 新建职位
  handleJobDescriptionCreate(fieldValues) {
    createJobDescription(fieldValues, (json) => {
      if (json.code === 200) {
        this.state.customerDataSource.map((item) => {
          if(item.id === json.data.info.company)
            json.data.info.company_name = item.name;
        })
        let array = new Array(json.data.info);
        console.log(array);
        this.setState({
          newjd: array
        },() => {this.getFastMatchingByID()});

        message.success(language.ACTION_SUCCESS);
      } else {

        message.error(language.ACTION_FAIL);
      }
    });
  }

  getFastMatchingByID() {
    const date = new Date();
    const defFilterData = {date: [moment(date).add(-180, 'days').format('YYYY-MM-DD'),
                                  moment(date).format('YYYY-MM-DD')]};

    // let promise = new Promise((resolve, reject) => {
    //   this.getLSIAllSIMSDataSource(resolve);
    // });
    let postAPI = API.LSI_BY_JD_ID_API;
        let array = new Array(StorageUtil.get("_pj"));
        let postData = {
            id: this.state.newjd[0].id,
            uses: array,
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
    }

  // getLSIAllSIMSDataSource(resolve) {
  //   getLSIAllSIMS(json => {
  //     if (json.code === 200) {
  //       this.setState({
  //         classify: json.classify,
  //         projects: json.projects
  //       });
  //       resolve(json.projects.concat(json.classify));
  //     }
  //   });
  // }

  // 获取渲染扩展JD展开行
  getExpandedRowRender(record) {
    console.log(record);
    return (
      <div>
        {record.description.split('\n').map((item, index) => { return (<p key={index}>{item}</p>); })}
      </div>
    )
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
      width: '15%'
    },{
      title: language.OPERATION,
      key: 'operation',
      width: '15%',
      render: (record) => (
        <Operation record={record}/>
      )
    }];
    return (
      <div className="cs-addposition">
      <ShowCard>
        <CreateNewJobDescription
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

        { this.state.newjd.length > 0 ?
        <div className="cs-addposition-result">
        <Table 
          dataSource={this.state.newjd} 
          columns={columns} 
          pagination={false}
          rowKey={record => record.id}
          defaultExpandAllRows={true}
          expandedRowRender={record => this.getExpandedRowRender(record)}
        />
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
          showPagination={false}
        />
        </div>
        : null
        }
      </ShowCard>
      </div>
    );
  }
}

export default AddPosition;