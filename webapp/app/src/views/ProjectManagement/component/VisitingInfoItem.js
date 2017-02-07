'use strict';
import React, { Component, PropTypes } from 'react';

import EnhancedInput from 'components/enhanced-input';

import { Button } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class VisitingInfoItem extends Component {
  constructor() {
    super();
    this.state = {
      editStatus: false,
      opening: false,
    };
    this.handleAddClick = this.handleAddClick.bind(this);
    this.handleDeleteClick = this.handleDeleteClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleOmmitClick = this.handleOmmitClick.bind(this);
    this.handleDoubleClick = this.handleDoubleClick.bind(this);
    this.getEditingRender = this.getEditingRender.bind(this);
    this.getRender = this.getRender.bind(this);
  }

  handleAddClick(value) {
    const { dataIndex, dataId } = this.props;

    if (value.trim() !== '') {
      this.props.onSave({
        id: dataId,
        fieldProp: dataIndex,
        fieldValue: value
      });
    }
  }

  handleDeleteClick(content, date) {
    const { dataId, dataIndex } = this.props;

    this.props.onRemove(dataId, dataIndex, content, date);
  }

  handleCancelClick() {
    this.setState({
      editStatus: false
    });
  }

  handleOmmitClick() {
    this.setState({
      opening: !this.state.opening
    });
  }

  handleDoubleClick() {
    this.setState({
      editStatus: true
    });
  }

  getEditingRender() {
    const { editStatus } = this.state;

    if (editStatus) {
      return (
        <div className="visiting-form">
          <EnhancedInput
            type="plus"
            size="small"
            style={{ display: 'inline-block', width: '80%' }}
            resettable={true}
            onClick={this.handleAddClick}
          />
          <Button
            size="small"
            onClick={this.handleCancelClick}
          >
           {language.CANCEL}
          </Button>
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
          className={opening ? 'company-item-cell' : 'company-item-cell ommit'}
          onClick={this.handleOmmitClick}
          onDoubleClick={this.handleDoubleClick}
        >
          {dataSource.length > 0 ?
            `${dataSource[0].author} | ${dataSource[0].date.split(' ')[0]} | ${dataSource[0].content}` :
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
        <div
          onDoubleClick={this.handleDoubleClick}
        >
          {dataSource.length > 0 ? 
            dataSource.map((item, index) => {
              return (
                <p key={index} className="visiting-list">
                  {`${item.author} | ${item.date.split(' ')[0]} | ${item.content}`}
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
        onDoubleClick={this.handleEditClick}
      >
        {this.getRender()}
        {this.getEditingRender()}
      </div>
    );
  }
}

VisitingInfoItem.defaultProps = {
  itemInfo: {},
  dataSource: [],
  onSave() {},
  onRemove() {}
};

VisitingInfoItem.propTypes = {
  dataId: PropTypes.string,
  dataIndex: PropTypes.string,
  visible: PropTypes.bool,
  dataSource: PropTypes.array,
  onSave: PropTypes.func,
  onRemove: PropTypes.func
};

export default VisitingInfoItem;
