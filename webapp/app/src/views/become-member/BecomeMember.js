'use strict';
import React, { Component } from 'react';

import { message, Card, Button,Icon,Form,Input } from 'antd';

import StorageUtil from 'utils/storage';
import { becomeMember } from 'request/member';

const FormItem = Form.Item;

class BecomeMenber extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      dataSource: '',
      projects: [],
    };
    this.handleBtnClick = this.handleBtnClick.bind(this);
  }

  handleBtnClick() {
    becomeMember({
      membername: StorageUtil.get('user')
    }, (json) => {
      if (json.code === 200) {
        message.success('注册成功',3,function(){
        });
      } else {
        message.error('注册信息有误！');
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
              <span>申请会员</span></h1>
              <p>会员让您尊享更加流畅更加精彩的高端服务</p>
              <p>从菜鸟到老司机，一个会员的距离。</p>
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
        </Form>
            <Button type="primary" onClick={this.handleBtnClick}>申请会员</Button>
          </div>
          </Card>
        </div>
      </div>
    );
  }
}

export default BecomeMenber = Form.create({})(BecomeMenber);