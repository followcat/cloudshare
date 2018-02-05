'use strcit';
import React, { Component } from 'react';
import { browserHistory } from 'react-router';

import { introJs } from 'intro.js';

import TablePlus from 'components/table-plus';
import SiderPanel from 'components/sider-panel';
import DetailInformation from 'components/detail-information';
import ButtonWithModal from 'components/button-with-modal';
import ExtractInfo from './ExtractInfo';

import {
  Popconfirm,
  Pagination,
  message,
  Select,
  Form,
  Spin
} from 'antd';

import {
  getCustomerList,
  updateCustomer,
  getAddedCompanyList,
  updateCompanyInfo,
  updateCompanyInfoList,
  deleteCompanyInfoList
} from 'request/company';

import find from 'lodash/find';
import Storage from 'utils/storage';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

let timer = null;

const extractValueToString = (key, array) => {
  if (array instanceof Array) {
    return array.map(v => v[key])
              .join(', ');
  }

  return '';
};

class Customer extends Component {
  constructor() {
    super();
    this.state = {
      user: Storage.get('user'),
      current: 1,
      totals: 0,
      pageSize: 10,
      dataSource: [],
      fetching: false,
      loading: false,
      visible: false,
      siderPanelVisible: false,
      guide: false,
      detailData: {},
      companyDataSource: [],
      value: '',
      id: ''
    };
    this.handleDeleteCustomerConfirm = this.handleDeleteCustomerConfirm.bind(this);
    this.handleViewDetailsClick = this.handleViewDetailsClick.bind(this);
    this.handleSiderPanelClose = this.handleSiderPanelClose.bind(this);
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleOkClick = this.handleOkClick.bind(this);
    this.handleExtractInfoCreate = this.handleExtractInfoCreate.bind(this);
    this.handleExtractInfoRemove = this.handleExtractInfoRemove.bind(this);
    this.handleBasicInfoSave = this.handleBasicInfoSave.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.getDataSource = this.getDataSource.bind(this);
    this.getCompanyDataSource = this.getCompanyDataSource.bind(this);
    this.getElements = this.getElements.bind(this);
    this.handleShowSizeChange = this.handleShowSizeChange.bind(this);
    this.handlePaginationChange = this.handlePaginationChange.bind(this);
  }

  handleDeleteCustomerConfirm(id) {
    updateCustomer('DELETE', {
      id: id
    }, (json) => {
      if (json.code === 200) {
        message.success(language.DELETE_SUCCESS_MSG);
        this.getDataSource();
      } else {
        message.error(language.DELETE_FAIL_MSG);
      }
    });
  }

  handleViewDetailsClick(record) {
    this.setState({
      siderPanelVisible: true,
      detailData: record
    });
  }

  handleSiderPanelClose() {
    this.setState({
      siderPanelVisible: false
    });
  }

  handleButtonClick() {
    this.setState({
      visible: true
    });
  }

  handleOkClick() {
    const { id } = this.state;
    updateCustomer('POST', {
      id: id
    }, (json) => {
      if (json.code === 200) {
        this.setState({ visible: false });
        message.success(language.ADD_SUCCESS_MSG);
        this.getDataSource();
      } else {
        message.error(language.ADD_FAIL_MSG);
      }
    });
  }

  handleCancelClick() {
    this.setState({
      visible: false
    });
  }

  handleExtractInfoCreate(data) {
    let key = Object.keys(data).filter((item) => {return item != 'id' && item != 'project'});
    key = key[0];
    let params = {};
        params['project'] = data.project;
        params['metadata'] = {[key]: {content: data[key], author: this.state.user},id: data.id};
    updateCompanyInfoList(params, (json) => {
      if (json.code === 200) {
        message.success('更新成功!');
        this.setState({
          siderPanelVisible: false,
          editStatus: false
        })
        this.getDataSource();
      } else {
        message.error('更新失败!');
      }
    });
  }

  handleExtractInfoRemove(key, value, date, id) {
    let params = {};
        params['metadata'] = {
          [key]: {content: value, author: this.state.user, date: date},
          id: id};
    deleteCompanyInfoList(params, (json) => {
      if (json.code === 200) {
        message.success('更新成功!');
          this.getDataSource();
        } else {
          message.error('更新失败!');
        }
    });
  }

  handleBasicInfoSave(data) {
    let params = {};
        params['metadata'] = data;
    updateCompanyInfo(params, (json) => {
        if (json.code === 200) {
          message.success('更新成功!');
          this.setState({
            siderPanelVisible: false,
            editStatus: false
          });
          this.getDataSource();
        } else {
          message.error('更新失败!');
        }
    });
  }

  handleChange = (value) => {
    const { companyDataSource } = this.state;
    this.setState({ 
      value: value,
      fetching: true
    });
    if(value.length > 0){
      this.getCompanyDataSource();
    } else {
      this.setState({
        companyDataSource: [],
        id: ''
      });
    }
  }

  handleShowSizeChange(current, pageSize) {
      this.setState({
        current: current,
        pageSize: pageSize
      },() => this.getDataSource());
  }

  handlePaginationChange(current) {
      this.setState({
        current: current
      },() => {this.getDataSource()});
  }

  getDataSource() {
    const { current,
            pageSize,} = this.state;
    this.setState({
      loading: true
    });

    getCustomerList({
      current_page: current,
      page_size: pageSize,
    },json => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          totals: json.totals,
          loading: false
        });
      }
    });
  }

  getCompanyDataSource() {
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
    timer = setTimeout(() => {
      getAddedCompanyList({
        text: this.state.value
      }, json => {
        if (json.code === 200) {
          this.setState({
            companyDataSource: json.data,
            fetching: false
          });
          let object = find(json.data,(item) => item.company_name === this.state.value);
          object && this.setState({
              id: object.id
          });
        }
      });
    }, 300);
  }

  getElements() {
    const {
      fetching,
      companyDataSource,
      visible,
    } = this.state;

    const elements = [{
      col: {
        span: 4
      },
      render: (
        <ButtonWithModal
          buttonStyle={{ marginLeft: 8 }}
          buttonType="primary"
          buttonText="新建已签约客户"
          visible={visible}
          modalTitle="新建已签约客户"
          modalOkText="提交"
          modalCancelText="取消"
          onButtonClick={this.handleButtonClick}
          onModalOk={this.handleOkClick}
          onModalCancel={this.handleCancelClick}
        >
          <Form>
            <Form.Item label="选择公司名称">
              <Select
                combobox
                value={this.state.value}
                defaultActiveFirstOption={false}
                showArrow={false}
                filterOption={false}
                onChange={this.handleChange}
              >
                { 
                  companyDataSource.map(item => {
                  return <Select.Option key={item.company_name}>{item.company_name}</Select.Option>
                })
                }
              </Select>
            </Form.Item>
          </Form>
        </ButtonWithModal>
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
    this.getDataSource();
    if(this.state.guide) {
      introJs().setOptions({
        'skipLabel': '退出', 
        'prevLabel':'上一步', 
        'nextLabel':'下一步',
        'doneLabel': '跳转到下个页面',
        'scrollToElement': false,
        steps: [                    
                    {
                        //第一步引导
                        element: '.cs-layout-subhead-customer',
                        intro: '已签约客户',
                        position: 'right'
                    },
                    {
                        element: '.ant-btn-primary',
                        intro: '确定新建客户存在于待开发客户中，不可重复创建！',
                        position: 'bottom'
                    }, 
                    {
                        //这个属性类似于jquery的选择器， 可以通过jquery选择器的方式来选择你需要选中的对象进行指引
                        element: '.ant-table-body',
                        //这里是每个引导框具体的文字内容，中间可以编写HTML代码
                        intro: '已签约客户展示',
                        //这里可以规定引导框相对于选中对象出现的位置 top,bottom,left,right
                        position: 'top'
                    },
                ]

      }).start().oncomplete(() => {  
          browserHistory.push('/pm/jobdescription?guide=true'); 
        });
      // introJs().start();
    }
  }

  render() {
    // 主体表格列数组
    const columns = [{
      title: language.COMPANY_NAME,
      dataIndex: 'name',
      key: 'name',
      width: '14%'
    }, {
      title: language.DISTRICT,
      dataIndex: 'district',
      key: 'district',
      width: '10%'
    }, {
      title: language.PRODUCT,
      dataIndex: 'product',
      key: 'product',
      width: '16%'
    }, {
      title: language.TELLPHONE,
      dataIndex: 'conumber',
      key: 'conumber',
      width: '12%'
    }, {
      title: language.EMAIL,
      dataIndex: 'email',
      key: 'email',
      width: '12%'
    }, {
      title: language.OPEN_POSITION,
      key: 'position',
      width: '14%',
      render: (text, record) => {
        return <span>{extractValueToString('content', record.position)}</span>;
      }
    }, {
      title: language.NEW_VISITING_SITUATION,
      key: 'progress',
      width: '12%',
      render: (text, record) => {
        return record.progress && record.progress.length > 0 ?
            <span>{record.progress[0].content}</span> :
            null;
      }
    }, {
      title: language.OPERATION,
      key: 'operation',
      width: '10%',
      render: (text, record) => {
        return (
          <ul>
            <li>
              <a
                href="javascript: void(0);"
                onClick={() => this.handleViewDetailsClick(record)}
              >
                {language.VIEW_DETAILS}
              </a>
            </li>
            <li>
              <Popconfirm
                title={language.DELETE_CONFIRM_MSG}
                onConfirm={() => this.handleDeleteCustomerConfirm(record.id)}
              >
                <a href="javascript: void(0);">
                  {language.DELETE}
                </a>
              </Popconfirm>
            </li>
          </ul>
        );
      }
    }];

    // 基本信息条目
    const rows = [{
      title: language.COMPANY_NAME,
      dataIndex: 'name',
      key: 'name'
    }, {
      title: language.PRODUCT,
      dataIndex: 'product',
      key: 'product'
    }, {
      title: language.TELLPHONE,
      dataIndex: 'conumber',
      key: 'conumber'
    }, {
      title: language.EMAIL,
      dataIndex: 'email',
      key: 'email'
    }, {
      title: language.ADDRESS,
      dataIndex: 'address',
      key: 'address'
    }, {
      title: language.WEBSITE,
      dataIndex: 'website',
      key: 'website',
      render: (record) => {
        return <a href={record} target="_blank">{record}</a>;
      }
    }, {
      title: language.COMPANY_INTRODUCTION,
      dataIndex: 'introduction',
      key: 'introduction',
      type: 'textarea'
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

    return (
      <div className="cs-Customer">
        <TablePlus
          rowKey={record => record.id}
          isToolbarShowed={true}
          isSearched={true}
          elements={this.getElements()}
          columns={columns}
          expandedRowRender={record => <p>{record.introduction}</p>}
          dataSource={this.state.dataSource}
          loading={this.state.loading}
        />
        <SiderPanel
          title={language.DETAILS_INFORMATION}
          visible={this.state.siderPanelVisible}
          onClose={this.handleSiderPanelClose}
        >
          <ExtractInfo 
            editable={true}
            title={language.EXTENDED_INFORMATION}
            dataSource={this.state.detailData}
            onCreate={this.handleExtractInfoCreate}
            onRemove={this.handleExtractInfoRemove}
          />
          <DetailInformation
            title={language.BASIC_INFORMATION}
            rows={rows}
            dataSource={this.state.detailData}
            editable={true}
            saveText={language.SAVE}
            cancelText={language.CANCEL}
            editText={language.EDIT}
            onSave={this.handleBasicInfoSave}
          />
        </SiderPanel>
        <div className="cs-card-inner-pagination">
          <Pagination {...pagination}/>
        </div>
      </div>
    );
  }
}

export default Customer;
