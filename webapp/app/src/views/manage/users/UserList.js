'use strict';
import React, { Component, PropTypes } from 'react';

import TablePlus from 'components/table-plus';
import CreateNewUser from './CreateNewUser';

import { Popconfirm, message } from 'antd';

import { deleteAccount } from 'request/account';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class UserList extends Component {
  constructor() {
    super();
    this.handleDeleteConfirm = this.handleDeleteConfirm.bind(this);
    this.getElements = this.getElements.bind(this);
    this.getColumns = this.getColumns.bind(this);
  }

  handleDeleteConfirm(userId) {
    deleteAccount(userId, (json) => {
      if (json.code === 200) {
        message.success(language.DELETE_SUCCESS_MSG);
        this.props.getUserList();
      } else {
        message.error(language.DELETE_FAIL_MSG);
      }
    });
  }

  getElements() {
    const elements = [{
      col: { span: 6 },
      render: (<CreateNewUser {...this.props}/>)
    }];

    return elements;
  }
  
  getColumns() {
    const columns = [{
      title: language.NAME,
      dataIndex: 'name',
      key: 'name',
      width: 300,
    }, {
      title: language.OPERATION,
      key: 'operation',
      render: (record) => (
        <Popconfirm
          title={language.DELETE_CONFIRM_MSG}
          onConfirm={() => this.handleDeleteConfirm(record.name)}
        >
          <a href="javascript: void(0);">{language.DELETE}</a>
        </Popconfirm>
      )
    }];

    return columns;
  }

  render() {
    const { dataSource, height } = this.props;

    return (
      <TablePlus
        dataSource={dataSource}
        isToolbarShowed={true}
        scroll={{ y: height }}
        elements={this.getElements()}
        columns={this.getColumns()}
      />
    );
  }
}

UserList.propTypes = {
  dataSource: PropTypes.any,
  height: PropTypes.number,
  getUserList: PropTypes.func
};

export default UserList;
