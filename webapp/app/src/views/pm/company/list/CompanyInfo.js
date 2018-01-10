'use strict';
import React, { Component, PropTypes } from 'react';

import BasicInfoItem from './BasicInfoItem';
import AdditionalInfoItem from './AdditionalInfoItem';
import VisitingInfoItem from './VisitingInfoItem';
import ReminderInfoItem from './ReminderInfoItem';
import Cell from './Cell';

import {
  Row,
  Col,
  Icon,
  Button,
  message
} from 'antd';

import { updateCompanyInfo, updateCompanyInfoList, deleteCompanyInfoList } from 'request/company';

import chunk from 'lodash/chunk';
import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class CompanyInfo extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      editStatus: false,
      formValues: {},
      deleteList: []
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleEditIconClick = this.handleEditIconClick.bind(this);
    this.handleUpdateFieldValues = this.handleUpdateFieldValues.bind(this);
    this.handleUpdateDeleteList = this.handleUpdateDeleteList.bind(this);
    this.handleSaveClick = this.handleSaveClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.getAdditionalInfoRender = this.getAdditionalInfoRender.bind(this);
    this.getBasicInfoOnExtra = this.getBasicInfoOnExtra.bind(this);
    this.getVisitingInfoRender = this.getVisitingInfoRender.bind(this);
  }

  handleClick() {
    this.setState({
      visible: !this.state.visible
    });
  }

  handleEditIconClick() {
    this.setState({
      visible: true,
      editStatus: true
    });
  }

  handleUpdateFieldValues(fieldProp, fieldValue) {
    const { formValues } = this.state;

    formValues[fieldProp] = fieldValue;
    this.setState({ formValues });
  }

  handleUpdateDeleteList(dataIndex, value) {
    const { deleteList } = this.state;

    deleteList.push({
      dataIndex: dataIndex,
      value: value
    });
    this.setState({ deleteList });
  }

  handleSaveClick() {
    const { dataSource } = this.props,
          { formValues, deleteList } = this.state;
    const listItemKeys = ['position', 'updatednumber', 'relatedcompany', 'clientcontact', 'reminder', 'progress'];

    let args = [],argslist = [],argslistdelete = [];

    for (let key in formValues) {
      let obj = {}, lbj = {};
      if (listItemKeys.indexOf(key) > -1) {
        lbj = {
          key: key,
        };
        lbj = Object.assign(lbj,formValues[key]);
        argslist.push(lbj);
      } else {
        obj = {
          key: key,
        };
        obj = Object.assign(obj,formValues[key]);
        args.push(obj);
      }
    }
    for (let i = 0; i < deleteList.length; i++) {
      let dlj = Object.assign({key: deleteList[i].dataIndex},deleteList[i].value);
      argslistdelete.push(dlj);
    }
    args.map( item => {
      let pram = Object.assign({id: dataSource.id},item)
      updateCompanyInfo(pram, (json) => {
        if (json.code === 200) {
          message.success('更新成功!');
          this.setState({
            formValues: [],
            deleteList: [],
            editStatus: false
          });
          this.props.updateDataSource();
        } else {
          message.error('更新失败!');
        }
      });
    })
    argslist.map( item => {
      let pram = Object.assign({id: dataSource.id},item)
      updateCompanyInfoList(pram, (json) => {
        if (json.code === 200) {
          message.success('更新成功!');
          this.setState({
            formValues: [],
            deleteList: [],
            editStatus: false
          });
          this.props.updateDataSource();
        } else {
          message.error('更新失败!');
        }
      });
    })
    argslistdelete.map( item => {
      let pram = Object.assign({id: dataSource.id},item)
      deleteCompanyInfoList(pram, (json) => {
        if (json.code === 200) {
          message.success('更新成功!');
          this.setState({
            formValues: [],
            deleteList: [],
            editStatus: false
          });
          this.props.updateDataSource();
        } else {
          message.error('更新失败!');
        }
      });
    })
  }

  handleCancelClick() {
    this.setState({
      editStatus: false
    });
  }

  getAdditionalInfoRender() {
    const additionalInfoRows = [{
      title: language.OPEN_POSITION,
      dataIndex: 'position',
      key: 'position'
    }, {
      title: language.CONTACT_WAY,
      dataIndex: 'updatednumber',
      key: 'updatednumber'
    }, {
      title: language.RELATED_COMPANY,
      dataIndex: 'relatedcompany',
      key: 'relatedcompany'
    }];

    const { editStatus } = this.state;

    return chunk(additionalInfoRows, 4).map((item, index) => {
      return (
        <Row key={index} className="extra-box">
          {item.map(item => {
            return (
              <Col span={24} key={item.key}>
                <AdditionalInfoItem
                  itemInfo={item}
                  dataSource={this.props.dataSource}
                  dataIndex={item.dataIndex}
                  editStatus={editStatus}
                  onUpdateFieldValues={this.handleUpdateFieldValues}
                  onUpdateDeleteList={this.handleUpdateDeleteList}
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
      title: language.DISTRICT,
      dataIndex: 'district',
      key: 'district'
    }, {
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

    const { editStatus } = this.state;

    return (
      <Row className="extra-box">
        {rows.map(item => {
          return (
            <Col span={24} key={item.key}>
              <BasicInfoItem
                labelCls="extra-label"
                key={item.key}
                itemInfo={item}
                dataSource={this.props.dataSource}
                dataIndex={item.dataIndex}
                editStatus={editStatus}
                onUpdateFieldValues={this.handleUpdateFieldValues}
                onUpdateDeleteList={this.handleUpdateDeleteList}
              />
            </Col>
          );
        })}
      </Row>
    );
  }

  getVisitingInfoRender() {
    const { dataSource } = this.props,
          { visible, editStatus } = this.state;

    return (
      <VisitingInfoItem
        visible={visible}
        dataSource={dataSource.progress}
        dataIndex="progress"
        editStatus={editStatus}
        onUpdateFieldValues={this.handleUpdateFieldValues}
        onUpdateDeleteList={this.handleUpdateDeleteList}
      />
    );
  }

  getReminderInfoRender() {
    const { dataSource } = this.props,
          { visible, editStatus } = this.state;
    
    return (
      <ReminderInfoItem
        visible={visible}
        dataSource={dataSource.reminder}
        dataIndex="reminder"
        editStatus={editStatus}
        onUpdateFieldValues={this.handleUpdateFieldValues}
        onUpdateDeleteList={this.handleUpdateDeleteList}
      />
    );
  }

  render() {
    const { dataSource } = this.props,
          { visible, editStatus } = this.state;

    const items = [{
      key: 'name',
      dataIndex: 'name',
      width: '28.61888888%',
      editable: false
    }, {
      key: 'clientcontact',
      dataIndex: 'clientcontact',
      width: '21.45999999%'
    }, {
      key: 'conumber',
      dataIndex: 'conumber',
      width: '21.45999999%'
    }, {
      key: 'responsible',
      dataIndex: 'responsible',
      width: '14.29999999%'
    }, {
      key: 'priority',
      dataIndex: 'priority',
      width: '14.15622222%'
    }];

    const expandCls = visible ? 'cs-row-expand-icon cs-row-expanded' : 'cs-row-expand-icon cs-row-collapsed';

    return (
      <div className="company-item">
        <Row className="company-item-row">
          <Col span="1" className="company-item-cell company-item-operation">
            <span className={expandCls} onClick={this.handleClick}></span>
            <span className="cs-row-expand-icon" onClick={this.handleEditIconClick}><Icon type="edit" /></span>
          </Col>
          <Col span="14">                                                                                                                                                                             
            <Row>
              {items.map(item => {
                return (
                  <Cell
                    {...item}
                    key={item.key}
                    dataSource={dataSource}
                    dataIndex={item.dataIndex}
                    editStatus={editStatus}
                    onUpdateFieldValues={this.handleUpdateFieldValues}
                    onUpdateDeleteList={this.handleUpdateDeleteList}
                  />
                );
              })}
            </Row>
            {visible ? this.getBasicInfoOnExtra() : null}
            {visible ? this.getAdditionalInfoRender() : null}
            {editStatus ?
              <div className="btn-group">
                <Button type="primary" size="small" onClick={this.handleSaveClick}>{language.SAVE}</Button>
                <Button size="small" onClick={this.handleCancelClick}>{language.CANCEL}</Button>
              </div> :
              null}
          </Col>
          <Col span="3" className="cell-item">
            {this.getReminderInfoRender()}
          </Col>
          <Col span="6" className="cell-item">
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
  dataSource: {}
};

CompanyInfo.propTypes = {
  isCustomer: PropTypes.bool,
  basicInfoRows: PropTypes.array,
  dataSource: PropTypes.object,
  updateDataSource: PropTypes.func,
};

export default CompanyInfo;
