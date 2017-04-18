'use strict';
import React, { Component, PropTypes } from 'react';

import { DatePicker, Input, Button } from 'antd';

import cloneDeep from 'lodash/cloneDeep';
import remove from 'lodash/remove';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

const t = 1000*60*60*24;

class ReminderInfoItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      opening: false,
      editStatus: false,
      datas: cloneDeep(props.dataSource),
      fieldValue: {
        content: '',
        date:''
      }
    };
    this.handleOmmitClick = this.handleOmmitClick.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.disabledDate = this.disabledDate.bind(this);
    this.getEditingRender = this.getEditingRender.bind(this);
    this.getRender = this.getRender.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.editStatus === false) {
      this.setState({
        datas: cloneDeep(nextProps.dataSource),
        fieldValue: {
          content: '',
          date: ''
        }
      });
    }
  }

  handleOmmitClick() {
    this.setState({
      opening: !this.state.opening
    });
  }

  handleDeleteClick(item) {
    const { dataIndex } = this.props,
          { datas } = this.state;

    remove(datas, (v) => {
      return v.author === item.author && v.content === item.content && v.date === item.date;
    });

    this.props.onUpdateDeleteList(dataIndex, item);
  }

  handleInputChange(e) { 
    const { fieldValue } = this.state,
          { dataIndex } = this.props;

    fieldValue.text = e.target.value;
    this.setState({ fieldValue });

    this.props.onUpdateFieldValues(dataIndex, { content: fieldValue });
  }

  handleDateChange(value, dateString) {
    const { fieldValue } = this.state,
          { dataIndex } = this.props;

    fieldValue.date = dateString;
    this.setState({ fieldValue });

    this.props.onUpdateFieldValues(dataIndex, { content: fieldValue });
  }

  disabledDate(current) {
    return current && current.value < Date.now() - t;
  }

  getEditingRender() {
    const { editStatus } = this.props;

    if (editStatus) {
      return (
        <div className="cs-reminder-edit-box">
          <Input
            size="small"
            onChange={this.handleInputChange}
          />
          <DatePicker
            size="small"
            disabledDate={this.disabledDate}
            onChange={this.handleDateChange}
          />
        </div>
      );
    }

    return null;
  }

  getRender() {
    const { visible, editStatus } = this.props,
          { datas, opening } = this.state;

    if (!visible) {
      return (
        <div
          className={opening ? '' : 'ommit'}
          onClick={this.handleOmmitClick}
        >
          {datas.length > 0 ?
            `${datas[0].author} | ${datas[0].content.date} | ${datas[0].content.text}` :
            `暂无数据`}
          {editStatus && datas.length > 0 ?
            <a
              className="visiting-list-del"
              href="javascript: void(0);"
              onClick={() => this.handleDeleteClick(datas[0])}>{language.DELETE}</a> :
            null}
        </div>
      );
    } else {
      return (
        <div>
          {datas.length > 0 ?
            datas.map((item, index) => {
              return (
                <p key={index} className="visiting-list">
                  {item.content && `${item.author} | ${item.content.date} | ${item.content.text}`}
                  {editStatus ?
                    <a
                      className="visiting-list-del"
                      href="javascript: void(0);"
                      onClick={() => this.handleDeleteClick(item)}>{language.DELETE}</a> :
                    null}
                </p>
              );
            }) :
           '暂无数据'}
        </div>
      );
    }
  }

  render() {
    return (
      <div
        className="cs-item-row"
        onDoubleClick={this.handleDoubleClick}
      >
        {this.getRender()}
        {this.getEditingRender()}
      </div>
    );
  }
}

ReminderInfoItem.propTypes = {
  visible: PropTypes.bool,
  editStatus: PropTypes.bool,
  dataSource: PropTypes.array,
  dataIndex: PropTypes.string,
  onUpdateFieldValues: PropTypes.func,
  onUpdateDeleteList: PropTypes.func
};

export default ReminderInfoItem;
