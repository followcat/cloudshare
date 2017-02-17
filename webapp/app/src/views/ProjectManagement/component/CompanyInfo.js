'use strict';
import React, { Component, PropTypes } from 'react';

import BasicInfoItem from './BasicInfoItem';
import AdditionalInfoItem from './AdditionalInfoItem';
import VisitingInfoItem from './VisitingInfoItem';
import Cell from './Cell';

import {
  Row,
  Col,
  Popconfirm
} from 'antd';

import chunk from 'lodash/chunk';
import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class CompanyInfo extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleConfirm = this.handleConfirm.bind(this);
    this.getRenderCustomerOperation = this.getRenderCustomerOperation.bind(this);
    this.getBasicInfoRender = this.getBasicInfoRender.bind(this);
    this.getAdditionalInfoRender = this.getAdditionalInfoRender.bind(this);
    this.getBasicInfoOnExtra = this.getBasicInfoOnExtra.bind(this);
    this.getVisitingInfoRender = this.getVisitingInfoRender.bind(this);
  }

  handleClick() {
    this.setState({
      visible: !this.state.visible
    });
  }

  handleConfirm(id) {
    this.props.onAddCustomerConfirm(id);
  }

  getRenderCustomerOperation() {
    const { dataSource, isCustomer } = this.props;

    if (isCustomer) {
      return <span style={{ color: 'green' }}>{language.ADDED_CUSTOMER}</span>;
    } else {
      return (
        <Popconfirm
          title={language.ADD_CONFIRM_MSG}
          onConfirm={() => this.handleConfirm(dataSource.id)}
        >
          <a href="javascript: void(0);">{language.ADD_CUSTOMER}</a>
        </Popconfirm>
      );
    }
  }

  getBasicInfoRender() {
    const basicInfoRows = [{
      title: language.COMPANY_NAME,
      dataIndex: 'name',
      key: 'name'
    }, {
      title: language.DISTRICT,
      dataIndex: 'district',
      key: 'district'
    }, {
      title: language.TELLPHONE,
      dataIndex: 'conumber',
      key: 'conumber'
    }];

    return chunk(basicInfoRows, 4).map((item, index) => {
      return (
        <Row key={index}>
          {item.map(v => {
            return (
              <Col span={8} key={v.key}>
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

    return chunk(additionalInfoRows, 4).map(item => {
      return (
        <Row className="extra-box">
          {item.map(v => {
            return (
              <Col span={24} key={v.dataIndex}>
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

  getBasicInfoOnExtra() {
    const rows = [{
      title: language.PRODUCT,
      dataIndex: 'product',
      key: 'product'
    }, {
      title: language.EMAIL,
      dataIndex: 'email',
      key: 'email'
    }, {
      title: language.ADDRESS,
      dataIndex: 'address',
      key: 'address'
    }, {
      title: language.WEBSITE,
      dataIndex: 'website',
      key: 'website',
      render: (record) => {
        return <a href={record} target="_blank">{record}</a>;
      }
    }, {
      title: language.COMPANY_INTRODUCTION,
      dataIndex: 'introduction',
      key: 'introduction',
      type: 'textarea'
    }];

    return (
      <Row className="extra-box">
        {rows.map(item => {
          return (
            <Col span={24} key={item.key}>
              <BasicInfoItem
                labelCls="extra-label"
                contentCls="extra-content"
                key={item.key}
                itemInfo={item}
                dataSource={this.props.dataSource}
                onSave={this.props.onSave}
              />
            </Col>
          );
        })}
      </Row>
    );
  }

  getVisitingInfoRender() {
    const { dataSource } = this.props,
          { visible } = this.state;

    return (
      <VisitingInfoItem
        visible={visible}
        dataSource={dataSource.progress}
        dataId={dataSource.id}
        dataIndex="progress"
        onSave={this.props.onSave}
        onRemove={this.props.onRemove}
      />
    );
  }

  render() {
    const { dataSource } = this.props,
          { visible } = this.state;

    const items = [{
      key: 'name',
      dataIndex: 'name',
      span: 12
    }, {
      key: 'clientcontact',
      dataIndex: 'clientcontact',
      span: 6
    }, {
      key: 'conumber',
      dataIndex: 'conumber',
      span: 6
    }];

    return (
      <div className="company-item">
        <Row className="company-item-row">
          <Col span="2" className="company-item-cell company-item-operation">
            {this.getRenderCustomerOperation()}
            <a href="javascript: void(0);" onClick={this.handleClick}>
              {visible ? language.FOLD_MSG : language.UNFOLD_MSG}
            </a>
          </Col>
          <Col span="10">
            <Row>
              {items.map(item => {
                return (
                  <Cell
                    key={item.key}
                    span={item.span}
                    dataSource={dataSource}
                    dataIndex={item.dataIndex}
                    onSave={this.props.onSave}
                    onRemove={this.props.onRemove}
                  />
                );
              })}
            </Row>
            {visible ? this.getBasicInfoOnExtra() : null}
            {visible ? this.getAdditionalInfoRender() : null}
          </Col>
          <Col span="12">
            {this.getVisitingInfoRender()}
          </Col>
        </Row>
      </div>
    );
  }
}

CompanyInfo.defaultProps = {
  isCustomer: false,
  basicInfoRows: [],
  dataSource: {},
  onSave() {},
  onRemove() {},
  onAddCustomerConfirm() {}
};

CompanyInfo.propTypes = {
  isCustomer: PropTypes.bool,
  basicInfoRows: PropTypes.array,
  dataSource: PropTypes.object,
  onSave: PropTypes.func,
  onRemove: PropTypes.func,
  onAddCustomerConfirm: PropTypes.func
};

export default CompanyInfo;
