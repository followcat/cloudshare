'use strict';
import React, { Component, PropTypes } from 'react';

import { DatePicker, Input, Button } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

const t = 1000*60*60*24;

class ReminderInfoItem extends Component {
  constructor() {
    super();
    this.state = {
      opening: false,
      editStatus: false,
      text: '',
      date: ''
    };
    this.handleDoubleClick = this.handleDoubleClick.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.disabledDate = this.disabledDate.bind(this);
    this.getEditingRender = this.getEditingRender.bind(this);
    this.getRender = this.getRender.bind(this);
  }

  handleDoubleClick() {
    this.setState({
      editStatus: true
    });
  }

  handleSave() {
    const { dataIndex, dataId } = this.props,
          { text, date } = this.state;

    if (text && date) {
      this.props.onSave({
        id: dataId,
        fieldProp: dataIndex,
        fieldValue: { text: text, date: date }
      });

      this.setState({
        editStatus: false
      });
    }
  }

  handleDeleteClick(content, date) {
    const { dataId, dataIndex } = this.props;

    this.props.onRemove(dataId, dataIndex, content, date);
  }

  handleCancel() {
    this.setState({
      editStatus: false
    });
  }

  handleInputChange(e) {
    this.setState({
      text: e.target.value
    });
  }

  handleDateChange(value, dateString) {
    this.setState({
      date: dateString
    });
  }

  disabledDate(current) {
    return current && current.getTime() < Date.now() - t;
  }

  getEditingRender() {
    const { editStatus } = this.state;

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
          <div className="cs-btn-group">
            <Button type="primary" size="small" onClick={this.handleSave}>{language.SAVE}</Button>
            <Button size="small" onClick={this.handleCancel}>{language.CANCEL}</Button>
          </div>
        </div>
      );
    }

    return null;
  }

  getRender() {
    const { visible, dataSource } = this.props,
          { opening, editStatus } = this.state;

    if (!visible) {
      return (
        <div
          className={opening ? '' : 'ommit'}
        >
          {dataSource.length > 0 ?
            `${dataSource[0].content.text} | ${dataSource[0].content.date}` :
            `暂无数据`}
          {editStatus && dataSource.length > 0 ?
            <a
              className="visiting-list-del"
              href="javascript: void(0);"
              onClick={() => this.handleDeleteClick(dataSource[0].content, dataSource[0].date)}>{language.DELETE}</a> :
            null}
        </div>
      );
    } else {
      return (
        <div>
          {dataSource.length > 0 ?
            dataSource.map((item, index) => {
              return (
                <p key={index} className="visiting-list">
                  {item.content && `${item.content.text} | ${item.content.date}`}
                  {editStatus ?
                    <a
                      className="visiting-list-del"
                      href="javascript: void(0);"
                      onClick={() => this.handleDeleteClick(item.content, item.date)}>{language.DELETE}</a> :
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
  dataSource: PropTypes.array,
  dataIndex: PropTypes.string,
  dataId: PropTypes.string,
  onSave: PropTypes.func,
  onRemove: PropTypes.func
};

export default ReminderInfoItem;
