'use strict';
import React, { Component, PropTypes } from 'react';

import BasicInfoItem from './BasicInfoItem';
import AdditionalInfoItem from './AdditionalInfoItem';
import VisitingInfoItem from './VisitingInfoItem';

import { Row, Col, Card } from 'antd';

import chunk from 'lodash/chunk';
import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;

class CompanyInfo extends Component {
  constructor() {
    super();
    this.getBasicInfoRender = this.getBasicInfoRender.bind(this);
    this.getAdditionalInfoRender = this.getAdditionalInfoRender.bind(this);
    this.getVisitingInfoRender = this.getVisitingInfoRender.bind(this);
  }

  getBasicInfoRender() {
    // 基本信息条目
    const basicInfoRows = [{
      title: language.COMPANY_NAME,
      dataIndex: 'name',
      key: 'name',
      editable: false
    }, {
      title: language.DISTRICT,
      dataIndex: 'district',
      key: 'district',
      editable: true
    }, {
      title: language.PRODUCT,
      dataIndex: 'product',
      key: 'product',
      editable: true
    }, {
      title: language.TELLPHONE,
      dataIndex: 'conumber',
      key: 'conumber',
      editable: true
    }, {
      title: language.EMAIL,
      dataIndex: 'email',
      key: 'email',
      editable: true
    }, {
      title: language.ADDRESS,
      dataIndex: 'address',
      key: 'address',
      editable: true
    }, {
      title: language.WEBSITE,
      dataIndex: 'website',
      key: 'website',
      render: (record) => {
        return <a href={record} target="_blank">{record}</a>
      },
      editable: true
    }, {
      title: language.COMPANY_INTRODUCTION,
      dataIndex: 'introduction',
      key: 'introduction',
      type: 'textarea',
      editable: true
    }];

    return chunk(basicInfoRows, 4).map((item, index) => {
      return (
        <Row key={index}>
          {item.map(v => {
            return (
              <Col span={6} key={v.key}>
                <BasicInfoItem
                  key={v.key}
                  itemInfo={v}
                  dataSource={this.props.dataSource}
                  onSave={this.props.onSave}
                />
              </Col>
            );
          })}
        </Row>
      );
    });
  }

  getAdditionalInfoRender() {
    const additionalInfoRows = [{
      title: language.OPEN_POSITION,
      dataIndex: 'position'
    }, {
      title: language.CONTACT,
      dataIndex: 'clientcontact'
    }, {
      title: language.CONTACT_WAY,
      dataIndex: 'updatednumber'
    }, {
      title: language.RELATED_COMPANY,
      dataIndex: 'relatedcompany'
    }];

    return chunk(additionalInfoRows, 4).map((item, index) => {
      return (
        <Row key={index}>
          {item.map(v => {
            return (
              <Col span={6} key={v.dataIndex}>
                <AdditionalInfoItem
                  key={v.dataIndex}
                  itemInfo={v}
                  dataSource={this.props.dataSource}
                  onSave={this.props.onSave}
                  onRemove={this.props.onRemove}
                />
              </Col>
            );
          })}
        </Row>
      );
    });
  }

  getVisitingInfoRender() {
    const itemInfo = {
      title: language.VISITING_SITUATION,
      dataIndex: 'progress'
    };

    return (
      <Row>
        <Col span={24}>
          <VisitingInfoItem
            itemInfo={itemInfo}
            dataSource={this.props.dataSource}
            onSave={this.props.onSave}
            onRemove={this.props.onRemove}
          />
        </Col>
      </Row>
    );
  }

  render() {
    return (
      <Card
        style={{ marginBottom: 8 }}
        bodyStyle={{ padding: 16 }}
      >
        {this.getBasicInfoRender()}
        {this.getAdditionalInfoRender()}
        {this.getVisitingInfoRender()}
      </Card>
    );
  }
}

CompanyInfo.defaultProps = {
  basicInfoRows: [],
  dataSource: {},
  onSave() {},
  onRemove() {}
};

CompanyInfo.propTypes = {
  basicInfoRows: PropTypes.array,
  dataSource: PropTypes.object,
  onSave: PropTypes.func,
  onRemove: PropTypes.func
};

export default CompanyInfo;
