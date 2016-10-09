'use strict';
import React, { Component } from 'react';
import { Link } from 'react-router';
import { Menu, message } from 'antd';
import 'whatwg-fetch';

import Header from '../components/common/Header';
import Storage from '../utils/storage';
import './manage.less';

export default class ListJD extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      current: 'jobdescription',
      jobDescriptionData: [],
      searchData: [],
      companyData: [],
      height: 0,
      confirmLoading: false,
      visible: false,
    };
    this.loadJobDescription = this.loadJobDescription.bind(this);
    this.loadCompany = this.loadCompany.bind(this);
    this.handleMenuClick = this.handleMenuClick.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleCreateNewJobDescription = this.handleCreateNewJobDescription.bind(this);
    this.handleSubmitEditJD = this.handleSubmitEditJD.bind(this);
    this.handleModalOpen = this.handleModalOpen.bind(this);
    this.handleModalCancel = this.handleModalCancel.bind(this);
    this.handleCreateNewCompany = this.handleCreateNewCompany.bind(this);
  }

  /**
   * 加载所有职位描述数据
   */
  loadJobDescription() {
    fetch(`/api/jdlist`, {
      method: 'GET',
      headers: {
        'Authorization': `Basic ${Storage.get('token')}`,
      },
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        let data = [];
        data = json.data.map((item, index) => {
          if (!item.key) {
            return Object.assign(item, { key: index });
          }
          return item;
        });
        this.setState({
          jobDescriptionData: data,
        });
      } else {
        console.log('Get jd error.');
      }
    })
  }

  /**
   * 加载所有公司数据
   */
  loadCompany() {
    fetch(`/api/companylist`, {
      method: 'GET',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
      },
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          companyData: json.data,
        });
      } else {
        console.log('Get company error.');
      }
    })
  }

  componentDidMount() {
    this.loadJobDescription();
    this.loadCompany();
    const height = parseInt(this.refs.wrapper.offsetHeight) - 208;
    this.setState({
      height: height,
    });
  }

  handleMenuClick(e) {
    this.setState({
      current: e.key,
    });
  }

  /**
   * 表格数据搜索
   * @param  {[string]} value [获取Input的值]
   * @return {[type]}  None
   */
  handleSearch(value) {
    let jdData = this.state.jobDescriptionData;
    if (value !== '') {
      let searchResultArray = [];
      for (let item of jdData) {
        for (let key in item) {
          if (typeof item[key] === 'string' && item[key].indexOf(value) > -1) {
            searchResultArray.push(item);
            break;
          }
        }
      }
      this.setState({
        searchData: searchResultArray,
      });
    } else {
      this.setState({
        searchData: [],
      });
    }
  }

  /**
   * 创建一个新的职位描述
   * @param  {[type]} object [获取表单数据对象]
   * @return {[type]} None
   */
  handleCreateNewJobDescription(obj) {
    const _this = this;
    this.setState({
      confirmLoading: true,
    });

    fetch(`/api/uploadjd`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        jd_name: obj.jdName,
        co_name: obj.companySelection,
        jd_description: obj.jdContent,
      }),
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          visible: false,
          confirmLoading: false,
        });
        message.success(json.message);
        _this.loadJobDescription();
      }
    })
  }

  /**
   * 修改Job Description
   * @param  {[object]}   value    [表单数据对象]
   * @param  {Function} callback [回调函数: 为了修改子组件state]
   * @return {[type]}  None
   */
  handleSubmitEditJD(value, callback) {
    const _this = this;
    fetch(`/api/jd/${value.jdId}`, {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Authroization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        status: value.statusSelect,
        coname: value.companyName,
        description: value.jdContent,
      }),
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        if (callback && typeof callback === 'function') {
          callback();
        }
        message.success(json.message);
        _this.loadJobDescription();
      }
    })
  }

  /**
   * 创建公司
   * @param  {[object]}   value    [表单数据对象]
   * @param  {Function} callback [回调函数: 为了修改子组件state]
   * @return {[type]}  None
   */
  handleCreateNewCompany(value, callback) {
    const _this = this;

    fetch(`/api/company`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authroization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        coname: value.companyName,
        introduction: value.introduction,
      }),
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        if (callback && typeof callback === 'function') {
          callback();
        }
        message.success(json.message);
        _this.loadCompany();
      }
    })
  }

  /**
   * Modal显示事件
   */
  handleModalOpen() {
    this.setState({
      visible: true,
    });
  }

  /**
   * Modal隐藏事件
   */
  handleModalCancel() {
    this.setState({
      visible: false,
    });
  }

  render() {
    return (
      <div>
        <div id="viewport">
          <Header fixed={true} />
          <div className="cs-layout-bottom">
            <div className="cs-layout-wrapper" ref="wrapper">
              <div className="cs-layout-sider">
                <Menu
                  mode="inline"
                  selectedKeys={[this.state.current]}
                  onClick={this.handleMenuClick}
                >
                  <Menu.Item key="jobdescription"><Link to="/jobdescription">Job Description</Link></Menu.Item>
                  <Menu.Item key="company"><Link to="/company">Company</Link></Menu.Item>
                </Menu>
              </div>
              <div className="cs-layout-content">
                {this.props.children && React.cloneElement(
                  this.props.children, {
                    jobDescriptionData: this.state.jobDescriptionData,
                    companyData: this.state.companyData,
                    searchData: this.state.searchData,
                    height: this.state.height,
                    confirmLoading: this.state.confirmLoading,
                    visible: this.state.visible,
                    onModalOpen: this.handleModalOpen,
                    onModalCancel: this.handleModalCancel,
                    onSearch: this.handleSearch,
                    onCreateNewJobDescription: this.handleCreateNewJobDescription,
                    onSubmitEditJD: this.handleSubmitEditJD,
                    onCreateNewCompany: this.handleCreateNewCompany,
                  })}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}