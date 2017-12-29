'use strict';
import React, { Component, PropTypes } from 'react';

import EnglishResumeAddition from './EnglishResumeAddition';
import DrawChart from './DrawChart';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

import {
  Row,
  Col,
  Checkbox,
  Button,
  Input,
  Form
} from 'antd';

import { URL } from 'URL';

class ResumeToolMenu extends Component {
  constructor() {
    super();
    this.state = {
      checked: false,
      name: '',
      source: '',
    };
    this.handleSwitchChange = this.handleSwitchChange.bind(this);
    this.hangdleSubmit = this.hangdleSubmit.bind(this);
    this.handleDownloadClick = this.handleDownloadClick.bind(this);
  }

  handleSwitchChange(e) {
    this.setState({
      checked: e.target.checked,
    });
  }

  hangdleSubmit(e) {
    e.preventDefault();
    const fieldValue = this.props.form.getFieldsValue();

    this.props.onSubmitModification(fieldValue);    
  }

  handleDownloadClick(e) {
    const { dataSource } = this.props;
    e.preventDefault();
    // 简历下载
    location.href = URL.getDownloadURL(dataSource.id);
  }

  render() {
    const {
      dataSource,
      resumeId,
      uploadProps,
      fileList
    } = this.props;

    const { getFieldDecorator } = this.props.form,
          style = this.state.checked ? { display: 'block' } : { display: 'none' };

    return (
      <div>
        <div className="tool-menu pd-lr-8">
          <Checkbox onChange={this.handleSwitchChange}>修改简历标题</Checkbox>
          <Button type="ghost" size="small" onClick={this.handleDownloadClick}>下载</Button>
          <EnglishResumeAddition
            resumeId={resumeId}
            uploadProps={uploadProps}
            fileList={fileList}
            onUploadModalOk={this.props.onUploadModalOk}
          />
        </div>
        <Form className="title-form pd-lr-8" style={style}>
          <Row>
            <Col span={8} className="title-wrapper">
              <Form.Item label="简历ID" prefixCls="title">
                <Input size="small" value={dataSource.id} readOnly={true} />
              </Form.Item>   
            </Col>
            <Col span={8} className="title-wrapper">
              <Form.Item label="姓名" prefixCls="title">
                {getFieldDecorator('name', {
                  initialValue: dataSource.name
                })(
                  <Input type="text" size="small" />
                )}
              </Form.Item>
            </Col>
            <Col span={8} className="title-wrapper">
              <Form.Item label="来源" prefixCls="title">
                {getFieldDecorator('origin', {
                  initialValue: dataSource.origin
                })(
                  <Input type="text" size="small" />
                )}
              </Form.Item>
            </Col>
          </Row>
          <Row>
            <Col span={2} offset={11}>
              <Button size="small" onClick={this.hangdleSubmit}>提交</Button>
            </Col>
          </Row>
        </Form>
      </div>
    );
  }
}

export default ResumeToolMenu = Form.create({})(ResumeToolMenu);

ResumeToolMenu.propTypes = {
  form: PropTypes.object,
  dataSource: PropTypes.object,
  resumeId: PropTypes.string,
  uploadProps: PropTypes.object,
  fileList: PropTypes.array,
  onSubmitModification: PropTypes.func,
  onUploadModalOk: PropTypes.func
};
