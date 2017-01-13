'use strict';
import React, { Component, PropTypes } from 'react';

import { Card, Button } from 'antd';

import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;

const kv = {
  name: language.COMPANY_NAME,
  district: language.DISTRICT,
  product: language.PRODUCT,
  conumber: language.TELLPHONE,
  email: language.EMAIL,
  address: language.ADDRESS,
  website: language.WEBSITE,
  introduction: language.COMPANY_INTRODUCTION,
  position: language.OPEN_POSITION,
  clientcontact: language.CONTACT,
  progress: language.VISITING_SITUATION,
  relatedcompany: language.RELATED_COMPANY,
  updatednumber: language.CONTACT_WAY
};

class CompanyUploader extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.onConfirmUpload();
  }

  render() {
    const { dataSource } = this.props;

    return (
      <div>
        <div className="card-inner-top">
          <div className="legend">
            <div className="legend-item">
              <div className="block bg-green"></div>
              <div className="legend-item-label">{language.NEW_CREATION}</div>
            </div>
            <div className="legend-item">
              <div className="block bg-yellow"></div>
              <div className="legend-item-label">{language.CHANGE}</div>
            </div>
          </div>
          <Button
            type="primary"
            loading={this.props.loading}
            onClick={this.handleClick}
          >
            {language.CONFIRM_UOLOAD}
          </Button>
        </div>
        {dataSource.map(item => {
          return (
            <Card key={item.id} className={item.type !== null ? 'company-item bg-green' : 'company-item'}>
              <div className="info">
                <label className="info-index">{language.COMPANY_NAME}</label>
                <span>{item.name}</span>
              </div>
              {item.diff && item.diff.map((diffItem, index) => {
                return (
                  <div key={index} className="diff bg-yellow">
                    <label className="diff-index">{kv[diffItem.dataIndex]}</label>
                    <span>{diffItem.value}</span>
                  </div>
                );
              })}
            </Card>
          );
        })}
      </div>
    );
  }
}

CompanyUploader.propTypes = {
  loading: PropTypes.bool,
  dataSource: PropTypes.array,
  onConfirmUpload: PropTypes.func
};

export default CompanyUploader;
