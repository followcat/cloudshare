'use strict';
import React, { Component } from 'react';

import { message, Card, Button,Icon,Form,Input } from 'antd';

import StorageUtil from 'utils/storage';
import { becomeMember } from 'request/member';

const FormItem = Form.Item;

class BecomeMember extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      dataSource: '',
      projects: [],
    };
    this.handleBtnClick = this.handleBtnClick.bind(this);
  }

  handleBtnClick(e) {
    e.preventDefault();

  this.props.form.validateFields((errors, values) => {
      if (!errors) {
        becomeMember({
      membername: values.membername
    }, (json) => {
      if (json.result === true) {
        StorageUtil.unset('_pj');
        message.success('成功！',2,function(){
          window.location.reload();
        });
      } else {
        message.error('失败！');
      }
    });
      }
    });
  }

  render() {
    const { getFieldDecorator } = this.props.form;

    return (
      <div className="cs-becomemember">
        <div className="cs-container">
          <Card>
          <div className="cs-container-center">
              <h1><Icon type="rocket" />
              <span>成为免费会员</span></h1>
              <p>创建组织，管理项目以及成员，上传云端职位以及简历。</p>
              <p>获得强大的智能分析和推荐功能。</p>
              <p>同时，我们将会保证数据的隐私安全。</p>
        <Form layout="horizontal" >
        <FormItem >
          {getFieldDecorator('membername',{
            rules: [{
              required: true, message: '该栏是必填项',}
            ],
          })(
            <Input placeholder="公司名称"/>
          )}
        </FormItem>
        <FormItem>
          <Button type="primary" onClick={this.handleBtnClick}>申请会员</Button>
        </FormItem>
        </Form>
          </div>
          </Card>
        </div>
      </div>
    );
  }
}

export default BecomeMember = Form.create({})(BecomeMember);