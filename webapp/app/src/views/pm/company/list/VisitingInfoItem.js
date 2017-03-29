'use strict';
import React, { Component, PropTypes } from 'react';

import { Input } from 'antd';

import cloneDeep from 'lodash/cloneDeep';
import remove from 'lodash/remove';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class VisitingInfoItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datas: cloneDeep(props.dataSource),
      opening: false,
      fieldValue: ''
    };
    this.handleDeleteClick = this.handleDeleteClick.bind(this);
    this.handleOmmitClick = this.handleOmmitClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.getEditingRender = this.getEditingRender.bind(this);
    this.getRender = this.getRender.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.editStatus === false) {
      this.setState({
        datas: cloneDeep(nextProps.dataSource),
        fieldValue: ''
      });
    }
  }

  handleChange(e) {
    const { dataIndex } = this.props;

    this.setState({
      fieldValue: e.target.value
    });

    this.props.onUpdateFieldValues(dataIndex, { content: e.target.value });
  }

  handleDeleteClick(item) {
    const { dataIndex } = this.props,
          { datas } = this.state;

    remove(datas, (v) => {
      return v.author === item.author && v.content === item.content && v.date === item.date;
    });

    this.props.onUpdateDeleteList(dataIndex, item);
  }

  handleOmmitClick() {
    this.setState({
      opening: !this.state.opening
    });
  }

  getEditingRender() {
    const { fieldValue } = this.state,
          { editStatus } = this.props;
    
    if (editStatus) {
      return (
        <div className="visiting-form">
          <Input value={fieldValue} size="small" onChange={this.handleChange} />
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
          className={opening ? 'company-item-cell' : 'company-item-cell ommit'}
          onClick={this.handleOmmitClick}
          onDoubleClick={this.handleDoubleClick}
        >
          {datas.length > 0 ?
            `${datas[0].author} | ${datas[0].date.split(' ')[0]} | ${datas[0].content}` :
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
        <div
          onDoubleClick={this.handleDoubleClick}
        >
          {datas.length > 0 ? 
            datas.map((item, index) => {
              return (
                <p key={index} className="visiting-list">
                  {`${item.author} | ${item.date.split(' ')[0]} | ${item.content}`}
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
        onDoubleClick={this.handleEditClick}
      >
        {this.getRender()}
        {this.getEditingRender()}
      </div>
    );
  }
}

VisitingInfoItem.defaultProps = {
  dataSource: []
};

VisitingInfoItem.propTypes = {
  dataIndex: PropTypes.string,
  visible: PropTypes.bool,
  editStatus: PropTypes.bool,
  dataSource: PropTypes.array,
  onUpdateFieldValues: PropTypes.func,
  onUpdateDeleteList: PropTypes.func
};

export default VisitingInfoItem;
