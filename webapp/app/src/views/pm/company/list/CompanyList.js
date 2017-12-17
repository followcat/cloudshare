'use strict';
import React, { Component, PropTypes } from 'react';
import { browserHistory } from 'react-router';

import CompanyInfo from './CompanyInfo';
import CreateNewCompany from './CreateNewCompany';
import FilterCondition from './FilterCondition';
import ButtonWithModal from 'components/button-with-modal';
import HeaderTitle from 'components/header-title';

import {
  Affix,
  message,
  Pagination,
  Spin,
  Upload,
  Button,
  Icon
} from 'antd';

import {
  getCustomerList,
  getAllCompany,
  getAllCompanyBySearch,
  createCompany,
} from 'request/company';

import cloneDeep from 'lodash/cloneDeep';
import remove from 'lodash/remove';
import findIndex from 'lodash/findIndex';
import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class CompanyList extends Component {
  constructor() {
    super();
    this.state = {
      current: 1,
      pageSize: 40,
      total: 0,
      dataSource: [],
      customerIDList: [],
      loading: false,
      visible: false,
      filterData: [{data:['name'],index:0}]
    };
    this.handleShowSizeChange = this.handleShowSizeChange.bind(this);
    this.handlePaginationChange = this.handlePaginationChange.bind(this);
    this.handleCreateCompanySubmit = this.handleCreateCompanySubmit.bind(this);
    this.handleUploadBtnClick = this.handleUploadBtnClick.bind(this);
    this.handleUploadModalCancel = this.handleUploadModalCancel.bind(this);
    this.handleUploadModalOk = this.handleUploadModalOk.bind(this);
    this.handleAddFilterCondition = this.handleAddFilterCondition.bind(this);
    this.handleFilterClick = this.handleFilterClick.bind(this);
    this.updateFilterCondition = this.updateFilterCondition.bind(this);
    this.updateDataSource = this.updateDataSource.bind(this);
    this.getDataSource = this.getDataSource.bind(this);
    this.getDataSourceBySearch = this.getDataSourceBySearch.bind(this);
  }

  componentDidMount() {
    const current = this.state.current,
          pageSize = this.state.pageSize;

    this.getDataSource(current, pageSize);
  }

  handleShowSizeChange(current, pageSize) {
    this.setState({
      current: current,
      pageSize: pageSize
    });

    if (this._isFilterValueNull()) {
      this.getDataSource(current, pageSize);
    } else {
      this.getDataSourceBySearch(current, pageSize);
    }
  }

  handlePaginationChange(current) {
    const { pageSize } = this.state;

    this.setState({
      current: current
    });

    if (this._isFilterValueNull()) {
      this.getDataSource(current, pageSize);
    } else {
      this.getDataSourceBySearch(current, pageSize);
    }
  }

  handleCreateCompanySubmit(fieldValues) {
    const { current, pageSize } = this.state;

    this.setState({
      createCompanyConfirmLoading: true
    });

    createCompany(fieldValues, (json) => {
      if (json.code === 200) {
        message.success(language.ADD_SUCCESS_MSG);
        this.getDataSource(current, pageSize);
      } else {
        message.error(language.ADD_FAIL_MSG);
      }
      this.setState({
        createCompanyConfirmLoading: false
      });
    });
  }

  handleUploadBtnClick() {
    this.setState({
      visible: true
    });
  }

  handleUploadModalCancel() {
    this.setState({
      visible: false
    });
  }

  handleUploadModalOk() {
    this.setState({
      visible: false
    });
    browserHistory.push('/pm/company/uploader');
  }

  handleAddFilterCondition(e) {
    e.preventDefault();
    const { filterData } = this.state;
    let datas = cloneDeep(filterData),
        len = datas.length;
    
    if (len > 0) {
      datas.push({
        index: datas[len - 1].index + 1,
        data: []
      });
    } else {
      datas.push({
        index: 0,
        data: []
      });
    }
  
    this.setState({
      filterData: datas
    });
  }

  handleFilterClick() {
    const { pageSize } = this.state,
      current = 1;
    
    this.setState({ current });

    if (this._isFilterValueNull()) {
      this.getDataSource(current, pageSize);
    } else {
      this.getDataSourceBySearch(current, pageSize);
    }
  }

  _isFilterValueNull() {
    const { filterData } = this.state;

    let data = filterData.map(v => v.data);

    for (var i = 0, len = data.length; i < len; i++) {
      if (typeof data[i][1] === 'undefined' || data[i][1] === '') {
        return true;
      }
    }

    return false;
  }

  updateFilterCondition(index, dataIndex, fieldValue = null) {
    const { filterData } = this.state;
    let datas = cloneDeep(filterData),
        i = findIndex(datas, (v) => v.index === index);

    switch(dataIndex) {
      case 'key':
        datas[i].data[0] = fieldValue;
        break;
      case 'value':
        datas[i].data[1] = fieldValue;
        break;
      case 'delete':
        remove(datas, (v) => v.index === index);
        break;
    }

    this.setState({
      filterData: datas
    });
  }

  updateDataSource() {
    const {
      current,
      pageSize
    } = this.state;
    
    if (this._isFilterValueNull()) {
      this.getDataSource(current, pageSize);
    } else {
      this.getDataSourceBySearch(current, pageSize);
    }
  }

  getDataSource(current, pageSize) {
    this.setState({
      loading: true
    });

    getAllCompany({
      current_page: current,
      page_size: pageSize
    }, (json) => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          total: json.total,
          loading: false
        });
      }
    });
  }

  getDataSourceBySearch(current, pageSize) {
    const { filterData } = this.state;
    let searchItems = filterData.map(v => v.data);

    this.setState({
      loading: true
    });

    getAllCompanyBySearch({
      current_page: current,
      page_size: pageSize,
      search_items: searchItems
    }, json => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          total: json.total,
          loading: false
        });
      }
    });
  }

  render() {
    const {
      current,
      total,
      pageSize,
      visible,
      filterData
    } = this.state;

    const { uploading, disabled } = this.props;

    // 主体表格分页
    const pagination = {
      current: current,
      total: total,
      pageSize: pageSize,
      showSizeChanger: true,
      showQuickJumper: true,
      defaultPageSize: 40,
      showTotal: total => `共 ${total} 条`,
      onShowSizeChange: this.handleShowSizeChange,
      onChange: this.handlePaginationChange
    };

    const headerTitle = [{
      key: 'opearator',
      span: 1
    },{
      key: 'name',
      text: language.COMPANY_NAME,
      span: 4,
    }, {
      key: 'clientcontact',
      text: language.CONTACT,
      span: 3
    }, {
      key: 'conumber',
      text: language.TELLPHONE,
      span: 3
    }, {
      key: 'responsible',
      text: language.RESPONSIBLE,
      span: 2
    }, {
      key: 'priority',
      text: language.PRIORITY,
      span: 2
    }, {
      key: 'reminder',
      text: language.REMINDER,
      span: 3
    }, {
      key: 'visiting',
      text: language.VISITING_SITUATION,
      span: 6
    }];
    return (
      <div className="cs-card-inner">
        <div className="cs-card-inner-top">
          <div className="cs-card-inner-top-col">
            <CreateNewCompany onSubmit={this.handleCreateCompanySubmit} />
          </div>
          <div className="cs-card-inner-top-col">
            <ButtonWithModal
              buttonText={language.UPLOAD}
              modalTitle={language.UPLOAD}
              visible={visible}
              disabled={disabled}
              onButtonClick={this.handleUploadBtnClick}
              onModalCancel={this.handleUploadModalCancel}
              onModalOk={this.handleUploadModalOk}
            >
              <Upload {...this.props.uploadProps}>
                <Button type="ghost">
                  <Icon type="upload" /> 点击上传
                </Button>
              </Upload>
              {uploading ? <Icon type="loading" className="uploading" /> : null}
            </ButtonWithModal>
          </div>
          <div className="cs-card-inner-top-filter">
            <label className="cs-label">过滤条件</label>
            {filterData.map((item) => {
              return (
                <FilterCondition
                  key={item.index}
                  index={item.index}
                  updateFilterCondition={this.updateFilterCondition}
                />
              );
            })}
            <a onClick={this.handleAddFilterCondition}>添加条件</a>
            <Button onClick={this.handleFilterClick}>{language.SUBMIT}</Button>
          </div>
        </div>
        <div className="cs-company-pagination">
          <Pagination {...pagination} />
        </div>
        <Spin
          size="large"
          spinning={this.state.loading}
        >
          <Affix>
            <HeaderTitle position="left" dataSource={headerTitle} />
          </Affix>
          {this.state.dataSource.map(item => {
            return (
              <CompanyInfo
                key={item.id}
                dataSource={item}
                isCustomer={this.state.customerIDList.indexOf(item.id) > -1}
                updateDataSource={this.updateDataSource}
              />
            );
          })}
        </Spin>
        <div className="cs-company-pagination">
          <Pagination {...pagination} />
        </div>
      </div>
    );
  }
}

CompanyList.defaultProps = {
  uploadProps: {}
};

CompanyList.propTypes = {
  uploadProps: PropTypes.object,
  uploading: PropTypes.bool,
  disabled: PropTypes.bool
};

export default CompanyList;
