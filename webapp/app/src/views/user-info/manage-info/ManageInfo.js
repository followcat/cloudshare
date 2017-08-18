'use strict';
import React, { Component, PropTypes } from 'react';

import Content from 'components/content';
import Info from 'components/manage-info';
import { updateInfo } from 'request/updateinfo';

import {
  message,
} from 'antd';

class ManageInfo extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      dataSource: '',
      projects: [],
    };
    this.handleManageInfoSubmit=this.handleManageInfoSubmit.bind(this);
  }

  handleManageInfoSubmit(feildValue){
    updateInfo({
      email: feildValue.email,
      phone: feildValue.phone,
    }, (json) => {
      if (json.code === 200) {
        message.success('更新成功',3,function(){
        });
      } else {
        message.error('更新失败！');
      }
    });
  }

  render() {
    const props = this.props;
    return (
      <Content prefixCls={props.prefixCls}>
        <Info onSubmit={this.handleManageInfoSubmit}/>
      </Content>
    );
  }
}

ManageInfo.defaultProps = {
  prefixCls: 'cs-manageinfo',
  onSubmit() {},
};

ManageInfo.propTypes = {
  onSubmit: PropTypes.func,
};

export default ManageInfo;
