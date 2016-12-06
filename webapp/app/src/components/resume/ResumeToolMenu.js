'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col, Checkbox, Button, Input, Form } from 'antd';

import EnglishResumeAddition from './EnglishResumeAddition';
import DrawChart from './DrawChart';
import { URL } from '../../config/url';

class ResumeToolMenu extends Component {

  constructor(props) {
    super(props);

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
    this.props.onModifyTitle(fieldValue);
  }

  handleDownloadClick(e) {
    e.preventDefault();
    this.props.onDownloadClick(this.props.dataSource.id);
  }

  render() {
    const { getFieldProps } = this.props.form,
          style = this.state.checked ? { display: 'block' } : { display: 'none' };

    return (
      <div>
        <div className="tool-menu pd-lr-8">
          <Checkbox onChange={this.handleSwitchChange}>Switch to Modify Title</Checkbox>
          <Button type="ghost" size="small" onClick={this.handleDownloadClick}>Download</Button>
          <EnglishResumeAddition
            style={{ display: 'inline-block', marginLeft: 4 }}
            upload={this.props.upload}
            fileList={this.props.fileList}
            enComfirmLoading={this.props.enComfirmLoading}
            onEnComfirmLoading={this.props.onEnComfirmLoading}
          />
          <DrawChart
            style={{ display: 'inline-block', marginLeft: 4 }}
            jdList={this.props.jdList}
            radarOption={this.props.radarOption}
            chartSpinning={this.props.chartSpinning}
            onDrawChartOpen={this.props.onDrawChartOpen}
            onDrawChartSubmit={this.props.onDrawChartSubmit}
          />
          <a
            style={{ display: 'inline-block', marginLeft: 4 }}
            href={URL.getFastMatchingByCV(this.props.dataSource.id)}
          >
            Fast Matching
          </a>
        </div>
        <Form className="title-form pd-lr-8" style={style}>
          <Row>
            <Col span={8} className="title-wrapper">
              <Form.Item
                label="ID"
                prefixCls="title"
              >
                <Input size="small" value={this.props.dataSource.id} readOnly={true} />
              </Form.Item>   
            </Col>
            <Col span={8} className="title-wrapper">
              <Form.Item
                label="Name"
                prefixCls="title"
              >
                <Input
                  {...getFieldProps('name', { initialValue: this.props.dataSource.name })}
                  type="text"
                  size="small"
                />
              </Form.Item>
            </Col>
            <Col span={8} className="title-wrapper">
              <Form.Item
                
                label="Source"
                prefixCls="title"
              >
                <Input
                  {...getFieldProps('origin', { initialValue: this.props.dataSource.origin })}
                  type="text"
                  size="small"
                />
              </Form.Item>
            </Col>
          </Row>
          <Row>
            <Col span={2} offset={11}>
              <Button size="small" onClick={this.hangdleSubmit}>Submit</Button>
            </Col>
          </Row>
        </Form>
      </div>
    );
  }
}

export default ResumeToolMenu = Form.create({})(ResumeToolMenu);

ResumeToolMenu.propTypes = {
  upload: PropTypes.object,
  dataSource: PropTypes.shape({
    id: PropTypes.string,
    name: PropTypes.string,
    origin: PropTypes.string,
  }),
  fileList: PropTypes.array,
  enComfirmLoading: PropTypes.bool,
  onEnComfirmLoading: PropTypes.func.isRequired,
  onModifyTitle: PropTypes.func.isRequired,
};
