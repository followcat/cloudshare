'use strcit';
import React, { Component } from 'react';

import TablePlus from 'components/table-plus';
import SiderPanel from 'components/sider-panel';
import DetailInformation from 'components/detail-information';
import ExtractInfo from './ExtractInfo';

import { Popconfirm, message } from 'antd';

import { getCustomerList, updateCustomer } from 'request/company';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

const extractValueToString = (key, array) => {
  return array.map(v => v[key])
              .join(', ');
};

class Customer extends Component {
  constructor() {
    super();
    this.state = {
      dataSource: [],
      loading: false,
      siderPanelVisible: false,
      detailData: {}
    };
    this.handleDeleteCustomerConfirm = this.handleDeleteCustomerConfirm.bind(this);
    this.handleViewDetailsClick = this.handleViewDetailsClick.bind(this);
    this.handleSiderPanelClose = this.handleSiderPanelClose.bind(this);
    this.getDataSource = this.getDataSource.bind(this);
  }

  componentDidMount() {
    this.getDataSource();
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

  getDataSource() {
    this.setState({
      loading: true
    });

    getCustomerList(json => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          loading: false
        });
      }
    });
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
        return record.progress.length > 0 ?
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
              <Popconfirm
                title={language.DELETE_CONFIRM_MSG}
                onConfirm={() => this.handleDeleteCustomerConfirm(record.id)}
              >
                <a href="javascript: void(0);">
                  {language.DELETE}
                </a>
              </Popconfirm>
            </li>
            <li>
              <a
                href="javascript: void(0);"
                onClick={() => this.handleViewDetailsClick(record)}
              >
                {language.VIEW_DETAILS}
              </a>
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

    return (
      <div>
        <TablePlus
          rowKey={record => record.id}
          isToolbarShowed={true}
          isSearched={true}
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
            editable={false}
            title={language.EXTENDED_INFORMATION}
            dataSource={this.state.detailData}
            onCreate={this.handleExtractInfoCreate}
            onRemove={this.handleExtractInfoRemove}
          />
          <DetailInformation
            title={language.BASIC_INFORMATION}
            rows={rows}
            dataSource={this.state.detailData}
            editable={false}
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

export default Customer;
