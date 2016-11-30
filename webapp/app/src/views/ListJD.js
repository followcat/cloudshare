'use strict';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';
import Viewport from '../components/viewport';
import Header  from '../components/header';
import CommonNavigation from './CommonNavigation';
import ShowCard from '../components/show-card';
import SiderMenu from '../components/sider-menu';
import Container from '../components/container';
import Content from '../components/content';
import CreateNewJobDescription from '../components/list-jd/CreateNewJobDescription';
import Status from '../components/list-jd/Status';
import EditJobDescription from '../components/list-jd/EditJobDescription';
import CreateNewCompany from '../components/list-jd/CreateNewCompany';
import { message } from 'antd';
import { getMenu, getCurrentActive } from '../utils/sider-menu-list';
import { getJobDescriptions, createJobDescription, updateJobDescription } from '../request/jobdescription';
import { getCompanys, createCompany } from '../request/company';
import { URL } from '../request/api';
import './list-jd.less';

class ListJD extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: getCurrentActive(props),
      statusValue: 'Opening',
      jobDescriptionList: [],
      filterList: [],
      companyList: [],
      height: 0,
      jdVisible: false,
      jdConfirmLoading: false,
      editConfirmLoading: false,
      companyConfirmLoading: false,
      companyVisible: false,
    };
    this.handleSiderMenuClick = this.handleSiderMenuClick.bind(this);
    this.handleNewJDBtnClick = this.handleNewJDBtnClick.bind(this);
    this.handleJDModalCancel = this.handleJDModalCancel.bind(this);
    this.handleJobDescriptionCreate = this.handleJobDescriptionCreate.bind(this);
    this.handleStatusChange = this.handleStatusChange.bind(this);
    this.handleEditJDSubmit = this.handleEditJDSubmit.bind(this);
    this.handleNewCompanyBtnClick = this.handleNewCompanyBtnClick.bind(this);
    this.handleCompanyModalCancel = this.handleCompanyModalCancel.bind(this);
    this.handleCompanyCreate = this.handleCompanyCreate.bind(this);
    this.getjobDescriptionList = this.getjobDescriptionList.bind(this);
    this.getCompanyList = this.getCompanyList.bind(this);
    this.getExpandedRowRender = this.getExpandedRowRender.bind(this);
    this.getJobDescriptionElements = this.getJobDescriptionElements.bind(this);
    this.getJobDescriptionColumns = this.getJobDescriptionColumns.bind(this);
    this.getCompanyElements = this.getCompanyElements.bind(this);
    this.getCompanyColumns = this.getCompanyColumns.bind(this);
  }

  componentDidMount() {
    this.getjobDescriptionList();
    this.getCompanyList();
    const eleShowCard = ReactDOM.findDOMNode(this.refs.showCard),
          height = eleShowCard.offsetHeight - 2*eleShowCard.offsetTop - 169;
    this.setState({
      height: height,
    });
  }

  // 侧边栏菜单点击切换光标
  handleSiderMenuClick(e) {
    this.setState({
      current: e.key,
    });
  }

  // 点击职位描述创建按钮, 打开Modal
  handleNewJDBtnClick() {
    this.setState({
      jdVisible: true,
    });
  }

  // 关闭职位描述Modal
  handleJDModalCancel() {
    this.setState({
      jdVisible: false,
    });
  }

  // 提交创建职位项目
  handleJobDescriptionCreate(value) {
    this.setState({
      jdConfirmLoading: true,
    });
    createJobDescription({
      co_id: value.companyName,
      jd_name: value.jobDescriptionName,
      jd_description: value.jobDescriptionContent,
    }, (json) => {
      if (json.code === 200) {
        this.setState({
          jdVisible: false,
          jdConfirmLoading: false,
        });
        message.success(json.message);
        this.getjobDescriptionList();
      } else {
        message.error(json.message);
      }
    });
  }

  // 职位项目状态切换,过滤列表
  handleStatusChange(value) {
    const jobDescriptionList = this.state.jobDescriptionList;
    let filterList = [];

    if (value) {
      filterList = jobDescriptionList.filter(item => {
        return item.status === value;
      });
    }

    this.setState({
      statusValue: value,
      filterList: filterList,
    });
  }

  // 提交修改职位信息
  handleEditJDSubmit(value) {
    this.setState({
      editConfirmLoading: true,
    });
    const params = {
      id: value.jobDescriptionID,
      co_id: value.company,
      description: value.jobDescriptionContent,
      status: value.status,
    };
    updateJobDescription(params, (json) => {
      if (json.code === 200) {
        this.getjobDescriptionList();
        this.setState({
          editConfirmLoading: false,
        });
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  // 点击公司创建按钮, 打开Modal
  handleNewCompanyBtnClick() {
    this.setState({
      companyVisible: true,
    });
  }

  // 关闭公司Modal
  handleCompanyModalCancel() {
    this.setState({
      companyVisible: false,
    });
  }

  // 提交创建公司
  handleCompanyCreate(value) {
    createCompany({
      coname: value.companyName,
      introduction: value.introduction,
    }, (json) => {
      if (json.code === 200) {
        this.setState({
          companyVisible: false,
        });
        message.success(json.message);
        this.getCompanyList();
      } else {
        message.error(json.message);
      }
    });
  }

  // 获取所有职位描述列表
  getjobDescriptionList() {
    const statusValue = this.state.statusValue;

    getJobDescriptions((json) => {
      if (json.code === 200) {
        this.setState({
          jobDescriptionList: json.data,
          filterList: json.data.filter(item => item.status === statusValue),
        });
      }
    });
  }

  // 获取所有公司列表
  getCompanyList() {
    getCompanys((json) => {
      if (json.code === 200) {
        this.setState({
          companyList: json.data,
        });
      }
    });
  }

  // 获取渲染扩展职位描述展开行
  getExpandedRowRender(record) {
    return record.description.split('\n').map((item, index) => {
      return <p key={index}>{item}</p>
    });
  }

  // 获取职位描述组件toolbar所要渲染组件
  getJobDescriptionElements() {
    const statusList = [{
      text: 'All',
      value: '',
    }, {
      text: 'Open',
      value: 'Opening',
    }, {
      text: 'Closed',
      value: 'Closed',
    }];

    const elements = [{
      col: {
        span: 3,
      },
      render: (
        <CreateNewJobDescription
          buttonStyle={{ marginLeft: 10 }}
          buttonType="primary"
          buttonText="Create"
          modalTitle="Create New Job Description"
          modalOkText="Create"
          confirmLoading={this.state.jdConfirmLoading}
          companyList={this.state.companyList}
          visible={this.state.jdVisible}
          onButtonClick={this.handleNewJDBtnClick}
          onModalCancel={this.handleJDModalCancel}
          onCreate={this.handleJobDescriptionCreate}
        />
      ),
    }, {
      col: {
        span: 4,
      },
      render: (
        <Status
          style={{ display: 'inline-block', marginLeft: 10 }}
          dataSource={statusList}
          width={120}
          defaultValue={this.state.statusValue}
          onChange={this.handleStatusChange}
        />
      )
    }];

    return elements;
  }

  // 获取职位描述列信息
  getJobDescriptionColumns() {
    const status = [{
      text: 'Open',
      value: 'Opening',
    }, {
      text: 'Closed',
      value: 'Closed',
    }];

    const columns = [{
      title: 'Company Name',
      dataIndex: 'company_name',
      key: 'company_name',
      width: 160,
    }, {
      title: 'Position',
      dataIndex: 'name',
      key: 'position',
      width: 240,
    }, {
      title: 'Creator',
      dataIndex: 'committer',
      key: 'creator',
      width: 80,
    }, {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (text) => {
        return text === 'Opening' ?
            <span style={{ color: 'green' }}>Open</span> :
            <span style={{ color: 'red' }}>{text}</span>
      }
    }, {
      title: 'Operation',
      key: 'operation',
      render: (record) => (
        <div>
          <a
            href={URL.getFastMatching(record.id)}
            target="_blank"
          >
            Fast Matching
          </a>
          <EditJobDescription
            buttonText="Edit"
            buttonSize="small"
            modalTitle="Edit Job Description"
            modalOkText="Submit"
            modalStyle={{ top: 20 }}
            record={record}
            companyList={this.state.companyList}
            status={status}
            confirmLoading={this.state.editConfirmLoading}
            onSubmit={this.handleEditJDSubmit}
          />
        </div>
      )
    }];
    return columns;
  }

  // 获取公司组件toolbar所要渲染组件
  getCompanyElements() {
    const elements = [{
      render: (
        <CreateNewCompany
          buttonType="primary"
          buttonText="Create"
          modalTitle="Create New Company"
          modalOkText="Create"
          confirmLoading={this.state.companyConfirmLoading}
          visible={this.state.companyVisible}
          onButtonClick={this.handleNewCompanyBtnClick}
          onModalCancel={this.handleCompanyModalCancel}
          onCreate={this.handleCompanyCreate}
        />
      ),
    }];

    return elements;
  }

  // 获取公司列信息
  getCompanyColumns() {
    const columns = [{
      title: 'Company Name',
      dataIndex: 'name',
      key: 'name',
      width: 280,
    },
    {
      title: 'Introduction',
      dataIndex: 'introduction',
      key: 'introduction',
    }];

    return columns;
  }

  render() {
    return (
      <Viewport>
        <Header 
          fixed={true}
          logoMode="left"
        >
          <CommonNavigation />
        </Header>
        <Container>
          <ShowCard ref="showCard">
            <SiderMenu
              selectedKeys={[this.state.current]}
              menus={getMenu(this.props.route.childRoutes)}
              onClick={this.handleSiderMenuClick}
            />
            <Content>
              {this.props.children && React.cloneElement(this.props.children, {
                jobDescriptionList: this.state.filterList.length > 0 ?
                    this.state.filterList :
                    this.state.jobDescriptionList,
                companyList: this.state.companyList,
                jobDescriptionColumns: this.getJobDescriptionColumns(),
                jobDescriptionElements: this.getJobDescriptionElements(),
                companyColumns: this.getCompanyColumns(),
                companyElements: this.getCompanyElements(),
                getExpandedRowRender: this.getExpandedRowRender,
                scroll: { y: this.state.height },
              })}
            </Content>
          </ShowCard>
        </Container>
      </Viewport>
    );
  }
}

export default ListJD;
