'use strict';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Header from 'components/header';
import Navigation from 'components/navigation';
import Viewport from 'components/viewport';
import Container from 'components/container';
import ShowCard from 'components/show-card';
import SiderMenu from 'components/sider-menu';
import Content from 'components/content';
import CreateNewUser from 'components/manage/CreateNewUser';
import Profile from 'components/manage/Profile';
import { message, Popconfirm, Menu, Modal } from 'antd';
import { getAccounts, createAccount, deleteAccount } from 'request/account';
import { resetPassword } from 'request/password';
import { signOut } from 'request/sign';
import { getMenu, getCurrentActive } from 'utils/sider-menu-list';
import './manage.less';

const MenuItem = Menu.Item,
      confirm = Modal.confirm;

export default class Manage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: getCurrentActive(props),
      dataSource: [],
      visible: false,
      confirmLoading: false,
      height: 0,
    };
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleCreate = this.handleCreate.bind(this);
    this.handleModalCancel = this.handleModalCancel.bind(this);
    this.handleDeleteConfirm = this.handleDeleteConfirm.bind(this);
    this.handleChangePasswordSubmit = this.handleChangePasswordSubmit.bind(this);
    this.handleSignOutConfirm = this.handleSignOutConfirm.bind(this);
    this.getUserList = this.getUserList.bind(this);
    this.getElements = this.getElements.bind(this);
    this.getColumns = this.getColumns.bind(this);
  }

  componentDidMount() {
    this.getUserList();
    const eleShowCard = ReactDOM.findDOMNode(this.refs.showCard),
          height = eleShowCard.offsetHeight - 2*eleShowCard.offsetTop - 169;

    this.setState({
      height: height,
    });
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.location.pathname !== this.props.location.pathname) {
      this.setState({
        current: getCurrentActive(this.props, nextProps),
      });
    }
  }

  handleButtonClick() {
    this.setState({
      visible: true,
    });
  }

  handleCreate(value) {
    this.setState({
      confirmLoading: true,
    });

    createAccount(value, (json) => {
      this.setState({
        confirmLoading: false,
        visible: false,
      });

      if (json.code === 200) {
        let datas = this.state.dataSource,
            len = datas.length;
        datas.unshift({ key: len, name: value.name });
        this.setState({
          dataSource: datas,
        });
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  handleModalCancel() {
    this.setState({
      visible: false,
    });
  }

  handleDeleteConfirm(userId) {
    deleteAccount(userId, (json) => {
      if (json.code === 200) {
        let datas = this.state.dataSource.filter(item => item.name !== userId);
        this.setState({
          dataSource: datas,
        });
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  handleChangePasswordSubmit(value) {
    const params = {
      oldpassword: value.oldPassword,
      newpassword: value.reNewPassword,
    };

    resetPassword(params, (json) => {
      if (json.code === 200) {
        message.success(json.message);
        setTimeout(() => {
          signOut((response) => {
            if (response.code === 200) {
              localStorage.removeItem('token');
              localStorage.removeItem('user');
              location.href = response.redirect_url;
            }
          });
        }, 1000);
      } else {
        message.error(json.message);
      }
    })
  }

  handleSignOutConfirm() {
    confirm({
      title: 'Sign out',
      content: 'Are you sure to sign out ?',
      onOk() {
        signOut((json) => {
          if (json.code === 200) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            location.href = json.redirect_url;
          }
        });
      },
      onCancel() {},
    });
  }
  
  getUserList() {
    getAccounts((json) => {
      if (json.code === 200) {
        let datas = json.data.map((value, index) => {
          return { key: index, name: value };
        });
        this.setState({
          dataSource: datas,
        });
      }
    });
  }

  getElements() {
    const elements = [{
      col: {
        span: 6
      },
      render: (
        <CreateNewUser
          dataSource={this.state.dataSource}
          buttonType="primary"
          buttonText="Create new user"
          onButtonClick={this.handleButtonClick}
          modalTitle="Create new user"
          modalOkText="Create"
          visible={this.state.visible}
          confirmLoading={this.state.confirmLoading}
          onCreate={this.handleCreate}
          onModalCancel={this.handleModalCancel}
        />
      )
    }];

    return elements;
  }

  getColumns() {
    const columns = [{
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      width: 300,
    }, {
      title: 'Operation',
      key: 'operation',
      render: (record) => (
        <Popconfirm
          title="Are you sure to delete this item ?"
          okText="Yes"
          cancelText="No"
          onConfirm={() => this.handleDeleteConfirm(record.name)}
        >
          <a href="#">Delete</a>
        </Popconfirm>
      )
    }];

    return columns;
  }

  render() {
    const dropdownMenu = (
      <Menu>
        <MenuItem key="0">
          <a href="#" onClick={this.handleSignOutConfirm}>Sign out</a>
        </MenuItem>
      </Menu>
    );

    const navs = [{
      key: 'profile',
      render: () => {
        return (
          <Profile 
            dropdownMenu={dropdownMenu}
            trigger={['click']}
            iconType="user"
            text={localStorage.user}
          />
        );
      },
    }];

    return (
      <Viewport>
        <Header fixed={true}>
          <Navigation navs={navs} />
        </Header>
        <Container>
          <ShowCard ref="showCard">
            <SiderMenu
              selectedKeys={[this.state.current]}
              menus={getMenu(this.props.route.childRoutes)}
            />
            <Content>
              {this.props.children && React.cloneElement(this.props.children, {
                dataSource: this.state.dataSource,
                columns: this.getColumns(),
                isToolbarShowed: true,
                elements: this.getElements(),
                scroll: { y: this.state.height },
                style: { paddingTop: 40 },
                onSubmit: this.handleChangePasswordSubmit
              })}
            </Content>
          </ShowCard>
        </Container>
      </Viewport>
    );
  }
}