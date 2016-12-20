'use strict';
import React, { Component } from 'react';

import TablePlus from '../../../components/table-plus';
import SiderPanel from '../../../components/sider-panel';
import EnhancedInput from '../../../components/enhanced-input';
import VisitingSituation from '../../../components/visiting-situation';
import DetailInformation from '../../../components/detail-information';
import CreateNewCompany from './CreateNewCompany';
import ExtractInfo from './ExtractInfo';

import { Button, message, Popconfirm } from 'antd';

import {
  getAllCompany,
  getAllCompanyBySearch,
  updateCompanyInfo,
  createCompany,
  getCustomerList,
  updateCustomer
} from '../../../request/company';
import StorageUtil from '../../../utils/storage';
import remove from 'lodash/remove';
import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;

const extractValueToString = (key, array) => {
  return array.map(v => v[key])
              .join(', ');
};

const fieldValuesToParams = (object) => {
  let arr = [];

  for (let k in object) {
    arr.push({ key: k, value: object[k] });
  }

  return arr;
}

export default class DevelopmentalCustomer extends Component {
  constructor() {
    super();
    this.state = {
      current: 1,
      pageSize: 10,
      total: 0,
      dataSource: [],
      detailData: {},
      customerIDList: [],
      searchWord: '',
      loading: false,
      siderPanelVisible: false,
      createCompanyConfirmLoading: false,
    };
    this.handleShowSizeChange = this.handleShowSizeChange.bind(this);
    this.handlePaginationChange = this.handlePaginationChange.bind(this);
    this.handleTablePlusSearch = this.handleTablePlusSearch.bind(this);
    this.handleViewDetailsClick = this.handleViewDetailsClick.bind(this);
    this.handleBasicInfoSave = this.handleBasicInfoSave.bind(this);
    this.handleSiderPanelClose = this.handleSiderPanelClose.bind(this);
    this.handleVisitingSubmit = this.handleVisitingSubmit.bind(this);
    this.handleExtractInfoCreate = this.handleExtractInfoCreate.bind(this);
    this.handleExtractInfoRemove = this.handleExtractInfoRemove.bind(this);
    this.handleCreateCompanySubmit = this.handleCreateCompanySubmit.bind(this);
    this.handleAddCustomerConfirm = this.handleAddCustomerConfirm.bind(this);
    this.getDataSource = this.getDataSource.bind(this);
    this.getDataSourceBySearch = this.getDataSourceBySearch.bind(this);
    this.getRenderCustomerOperation = this.getRenderCustomerOperation.bind(this);
  }

  componentDidMount() {
    const current = this.state.current,
          pageSize = this.state.pageSize;
    this.getDataSource(current, pageSize);
    this.getCustomerDataSource();
  }

  handleShowSizeChange(current, pageSize) {
    const searchWord = this.state.searchWord.trim();

    this.setState({
      current: current,
      pageSize: pageSize,
    });

    if (searchWord === '') {
      this.getDataSource(current, pageSize);
    } else {
      this.getDataSourceBySearch(searchWord, current, pageSize);
    }
  }

  handlePaginationChange(current) {
    const pageSize = this.state.pageSize,
          searchWord = this.state.searchWord.trim();
    this.setState({
      current: current,
    });

    if (searchWord === '') {
      this.getDataSource(current, pageSize);
    } else {
      this.getDataSourceBySearch(searchWord, current, pageSize);
    }
    
  }

  handleTablePlusSearch(value) {
    const pageSize = this.state.pageSize,
          current = 1;

    this.setState({
      searchWord: value,
      loading: true,
      current: current,
      pageSize: pageSize,
    });

    if (value) {
      this.getDataSourceBySearch(value, current, pageSize);
    } else {
      this.getDataSource(current, pageSize);
    }
  }

  handleViewDetailsClick(record) {
    this.setState({
      siderPanelVisible: true,
      detailData: record,
    });
  }

  handleBasicInfoSave(fieldValues) {
    const detailData = this.state.detailData,
          id = detailData.id;

    updateCompanyInfo('PUT', {
      id: id,
      update_info: fieldValuesToParams(fieldValues)
    }, (json) => {
      if (json.code === 200) {
        this.setState({
          detailData: Object.assign({}, detailData, json.data)
        });
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  handleSiderPanelClose() {
    this.setState({
      siderPanelVisible: false,
    });
  }

  handleVisitingSubmit(fieldValue) {
    console.log(fieldValue);
    let detailData = this.state.detailData,
        key = 'progress';

    updateCompanyInfo('PUT', {
      id: detailData.id,
      update_info: [{ key: key, value: fieldValue }]
    }, (json) => {
      if (json.code === 200) {
        detailData[key].unshift(json.data);
        this.setState({
          detailData: detailData
        });
        this.getDataSource(this.state.current, this.state.pageSize);
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  handleExtractInfoCreate(fieldValue) {
    let detailData = this.state.detailData,
        params = [];
    const key = Object.keys(fieldValue)[0];
    params.push({
      key: key,
      value: fieldValue[key]
    });
    updateCompanyInfo('PUT', {
      id: detailData.id,
      update_info: params
    }, (json) => {
      if (json.code === 200) {
        detailData[key].push(json.data);
        this.setState({
          detailData: detailData
        });
        this.getDataSource(this.state.current, this.state.pageSize);
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  handleExtractInfoRemove(key, value, date) {
    let detailData = this.state.detailData,
        data = detailData[key];

    updateCompanyInfo('DELETE', {
      id: detailData.id,
      key: key,
      value: value,
      date: date
    }, (json) => {
      if (json.code === 200) {
        let newData = remove(data, v => v.date !== json.data.date),
            newObj = {};
        newObj[key] = newData;
        this.setState({
          detailData: Object.assign({}, detailData, newObj),
        });
        this.getDataSource(this.state.current, this.state.pageSize);
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  handleCreateCompanySubmit(fieldValues) {
    const { current, pageSize } = this.state;
          
    this.setState({
      createCompanyConfirmLoading: true,
    });

    createCompany(fieldValues, (json) => {
      if (json.code === 200) {
        message.success(json.message);
        this.getDataSource(current, pageSize);
      } else {
        message.error(json.message);
      }
      this.setState({
        createCompanyConfirmLoading: false,
      });
    });
  }

  handleAddCustomerConfirm(id) {
    let idList = this.state.customerIDList;

    updateCustomer('POST', {
      id: id
    }, (json) => {
      if (json.code === 200) {
        message.success(language.ADD_SUCCESS_MSG);
        idList.push(id);
        this.setState({
          customerIDList: idList
        });
      } else {
        message.success(language.ADD_FAIL_MSG);
      }
    });
  }

  getDataSource(current, pageSize) {
    this.setState({
      loading: true,
    });

    getAllCompany({
      current_page: current,
      page_size: pageSize,
    }, (json) => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          total: json.total,
          loading: false,
        });
      }
    });
  }

  getDataSourceBySearch(searchWord, current, pageSize) {
    const dataSource = this.state.dataSource;

    this.setState({
      loading: true,
    });

    getAllCompanyBySearch({
      current_page: current,
      page_size: pageSize,
      search_text: searchWord
    }, json => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          total: json.total,
          loading: false,
        })
      }
    });
  }

  getCustomerDataSource() {
    getCustomerList(json => {
      if (json.code === 200) {
        let idList = json.data.map(v => v.id);
        this.setState({
          customerIDList: idList
        });
      } else {
        console.log('Get customer list error.')
      }
    })
  }

  getRenderCustomerOperation(id) {
    const idList = this.state.customerIDList;

    if (idList.indexOf(id) > -1) {
      return <span>{language.ADDED_CUSTOMER}</span>
    } else {
      return (
        <Popconfirm
          title={language.ADD_CONFIRM_MSG}
          onConfirm={() => this.handleAddCustomerConfirm(id)}
        >
          <a href="javascript: void(0);">{language.ADD_CUSTOMER}</a>
        </Popconfirm>
      )
    }
  }

  render() {

    // 表格头部工具栏元素数组
    const elements = [{
      col: { span: 6 },
      render: (
        <EnhancedInput
          type="search"
          style={{ marginRight: 8 }}
          onClick={this.handleTablePlusSearch}
        />
      )
    }, {
      col: { span: 3 },
      render: (
        <CreateNewCompany
          confirmLoading={this.state.createCompanyConfirmLoading}
          onSubmit={this.handleCreateCompanySubmit}
        />
      )
    }];

    // 主体表格列数组
    const columns = [{
      title: language.COMPANY_NAME,
      dataIndex: 'name',
      key: 'name',
      width: '14%',
    }, {
      title: language.PRODUCT,
      dataIndex: 'product',
      key: 'product',
      width: '20%'
    }, {
      title: language.TELLPHONE,
      dataIndex: 'conumber',
      key: 'conumber',
      width: '14%',
    }, {
      title: language.EMAIL,
      dataIndex: 'email',
      key: 'email',
      width: '12%',
    }, {
      title: language.OPEN_POSITION,
      key: 'position',
      width: '16%',
      render: (text, record) => {
        return <span>{extractValueToString('content', record.position)}</span>
      }
    }, {
      title: language.NEW_VISITING_SITUATION,
      key: 'progress',
      width: '14%',
      render: (text, record) => {
        return record.progress.length > 0 ?
            <span>{record.progress[0].content}</span> :
            null
      }
    }, {
      title: language.OPERATION,
      key: 'operation',
      width: '10%',
      render: (text, record) => {
        return (
          <ul>
            <li style={{ marginBottom: 8 }}>
              {this.getRenderCustomerOperation(record.id)}
            </li>
            <li><a href="javascript: void(0);" onClick={() => this.handleViewDetailsClick(record)}>{language.VIEW_DETAILS}</a></li>
          </ul>
        );
      }
    }];

    // 主体表格分页
    const pagination = {
      current: this.state.current,
      total: this.state.total,
      showSizeChanger: true,
      showQuickJumper: true,
      showTotal: total => `共 ${total} 条`,
      onShowSizeChange: this.handleShowSizeChange,
      onChange: this.handlePaginationChange
    }

    // 陌拜表列
    const visitingColumn = [{
      title: language.VISITING_SITUATION,
      dataIndex: 'content',
      key: 'situation',
      width: '60%',
    }, {
      title: language.DATE,
      dataIndex: 'date',
      key: 'date',
      width: '30%',
    }, {
      title: language.VISITOR,
      dataIndex: 'author',
      key: 'name',
      width: '10%',
    }];

    // 基本信息条目
    const rows = [{
      title: language.COMPANY_NAME,
      dataIndex: 'name',
      key: 'name',
    }, {
      title: language.DISTRICT,
      dataIndex: 'district',
      key: 'district',
    }, {
      title: language.PRODUCT,
      dataIndex: 'product',
      key: 'product',
    }, {
      title: language.TELLPHONE,
      dataIndex: 'conumber',
      key: 'conumber',
    }, {
      title: language.EMAIL,
      dataIndex: 'email',
      key: 'email',
    }, {
      title: language.ADDRESS,
      dataIndex: 'address',
      key: 'address',
    }, {
      title: language.WEBSITE,
      dataIndex: 'website',
      key: 'website',
      render: (record) => {
        return <a href={record} target="_blank">{record}</a>
      }
    }, {
      title: language.COMPANY_INTRODUCTION,
      dataIndex: 'introduction',
      key: 'introduction',
      type: 'textarea',
    }];

    return (
      <div>
        <TablePlus
          rowKey={record => record.id}
          isToolbarShowed={true}
          elements={elements}
          columns={columns}
          expandedRowRender={record => <p>{record.introduction}</p>}
          dataSource={this.state.dataSource}
          loading={this.state.loading}
          pagination={pagination}
        />
        <SiderPanel
          title={language.DETAILS_INFORMATION}
          visible={this.state.siderPanelVisible}
          onClose={this.handleSiderPanelClose}
        >
          <VisitingSituation
            title={language.VISITING_INFORMATION}
            columns={visitingColumn}
            dataSource={this.state.detailData.progress}
            pagination={false}
            currentUser={StorageUtil.get('user')}
            btnText={language.SUBMIT}
            onSubmit={this.handleVisitingSubmit}
          />
          <ExtractInfo 
            title={language.EXTENDED_INFORMATION}
            editable={true}
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
      </div>
    );
  }
}