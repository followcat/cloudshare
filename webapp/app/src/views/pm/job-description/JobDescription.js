'use strict';
import React, { Component } from 'react';
import { browserHistory } from 'react-router';

import TablePlus from 'components/table-plus';
import EditJobDescriptionForm from './EditJobDescriptionForm';
import CreateNewJobDescription from './CreateNewJobDescription';
import Status from './Status';
import Operation from './Operation';

import { introJs } from 'intro.js';

import { message, Pagination, } from 'antd';

import findIndex from 'lodash/findIndex';

import {
  getJobDescriptionList,
  getJobDescription,
  updateJobDescription,
  createJobDescription
} from 'request/jobdescription';
import { getCustomerList } from 'request/company';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class JobDescription extends Component {
  constructor() {
    super();
    this.state = {
      current: 1,
      totals: 0,
      pageSize: 10,
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
    this.getJobDescriptionByID = this.getJobDescriptionByID.bind(this);
    this.getExpandedRowRender = this.getExpandedRowRender.bind(this);
    this.getJobDescriptionElements = this.getJobDescriptionElements.bind(this);
    this.handleShowSizeChange = this.handleShowSizeChange.bind(this);
    this.handlePaginationChange = this.handlePaginationChange.bind(this);
  }

  handleEditClick(record) {
    this.getJobDescriptionByID(record.id);
    this.setState({
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
      status: fieldValues.status,
      commentary: fieldValues.commentary,
      followup: fieldValues.followup
    };

    updateJobDescription(params, (json) => {
      if (json.code === 200) {
        this.getjobDescriptionDataSource();
        this.setState({
          editConfirmLoading: false,
          editVisible: false
        });
        message.success(language.ACTION_SUCCESS);
      } else {
        this.setState({
          editConfirmLoading: false
        });
        message.error(language.ACTION_FAIL);
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
        message.success(language.ACTION_SUCCESS);
      } else {
        this.setState({
          jdConfirmLoading: false
        });
        message.error(language.ACTION_FAIL);
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
    },() => this.getjobDescriptionDataSource());
  }

  handleShowSizeChange(current, pageSize) {
      this.setState({
        current: current,
        pageSize: pageSize
      },() => this.getjobDescriptionDataSource());
  }

  handlePaginationChange(current) {
      this.setState({
        current: current
      },() => {this.getjobDescriptionDataSource()});
  }

  // 获取所有JD列表
  getjobDescriptionDataSource() {
    const { dataSource,
            filterDataSource,
            current,
            pageSize,
            statusValue } = this.state;
    
    this.setState({
      loading: true
    });
    
    getJobDescriptionList({
      status: statusValue,
      current_page: current,
      page_size: pageSize,
    },(json) => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          filterDataSource: json.data.filter(item => item.status === statusValue),
          loading: false,
          totals: json.totals
        });
      }
    });
  }

  // 根据id获取最新数据
  getJobDescriptionByID(id) {
    let { dataSource,filterDataSource, pageSize } = this.state;

    getJobDescription({
      'jd_id': id
    }, json => {
      if (json.code === 200) {
        const dataIndex = findIndex(dataSource, item => item.id === id),
              filterIndex = findIndex(filterDataSource, item => item.id === id);
        if (dataIndex > -1) {
          dataSource[dataIndex] = json.data;
          this.setState({
            dataSource: dataSource
          });
        }

        if (filterIndex > -1) {
          filterDataSource[filterIndex] = json.data;
          this.setState({
            filterDataSource: filterDataSource
          });
        }
      
        this.setState({
          record: json.data
        });
      }
    });
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

  // 获取渲染扩展JD展开行
  getExpandedRowRender(record) {
    return (
      <div>
        <div>
          {record.description.split('\n').map((item, index) => { return (<p key={index}>{item}</p>); })}
        </div>
        <div className="commentary-box">
          <label>{`${language.REMARKS}：`}</label>
          <p>{record.followup}</p>
        </div>
        <div className="commentary-box">
          <label>{`${language.COMMENTARY}：`}</label>
          {record.commentary && record.commentary.split('\n').map((item, index) => {
            return (
              <p key={index}>{item}</p>
            );
          })}
        </div>
      </div>
    );
  }

  // 获取职位描述组件toolbar所要渲染组件
  getJobDescriptionElements() {
    const statusList = [{
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

  componentWillMount() {
    if(this.props.location.query.guide) {
      this.setState({
      guide: this.props.location.query.guide
      })
    }
  }

  componentDidMount() {
    this.getjobDescriptionDataSource();
    this.getCustomerDataSource();
    if(this.state.guide) {
      introJs().setOptions({
        'skipLabel': '退出', 
        'prevLabel':'上一步', 
        'nextLabel':'下一步',
        'doneLabel': '完成',
        'scrollToElement': false,
        steps: [                    
                    {
                        //第一步引导
                        element: '.cs-layout-subhead-jobdescription',
                        intro: '已开放职位',
                        position: 'right'
                    },
                    {
                        //第三步引导
                        element: '.ant-btn-primary',
                        intro: '新建开放职位！',
                        position: 'bottom'
                    },
                    {
                        //这个属性类似于jquery的选择器， 可以通过jquery选择器的方式来选择你需要选中的对象进行指引
                        element: '.cs-job-description',
                        //这里是每个引导框具体的文字内容，中间可以编写HTML代码
                        intro: '新建职位结果展示，且可以进行快速匹配!',
                        //这里可以规定引导框相对于选中对象出现的位置 top,bottom,left,right
                        position: 'top'
                    },
                ]

      }).start().oncomplete(() => {  
          browserHistory.push('/pm/company/list'); 
        });
    }
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
        <Operation 
          record={record}
          onEdit={this.handleEditClick}
        />
      )
    }];

    const { current, totals, pageSize } = this.state;
    // 主体表格分页
    const pagination = {
      current: current,
      total: totals,
      pageSize: pageSize,
      showSizeChanger: true,
      showQuickJumper: true,
      defaultPageSize: 20,
      showTotal: totals => `共 ${totals} 条`,
      onShowSizeChange: this.handleShowSizeChange,
      onChange: this.handlePaginationChange
    };

    const state = this.state;

    return (
      <div className="cs-job-description">
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
        <div className='cs-job-description-result'>
        <EditJobDescriptionForm
          visible={state.editVisible}
          confirmLoading={state.editConfirmLoading}
          onSubmit={this.handleEditJobDescriptionSubmit}
          onCancel={this.handleEditFormCancel}
          record={this.state.record}
          customerDataSource={this.state.customerDataSource}
        />
        </div>
        <div className="cs-card-inner-pagination">
          <Pagination {...pagination}/>
        </div>
      </div>
    );
  }
}

export default JobDescription;
