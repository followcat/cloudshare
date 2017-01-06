'use strict';
import React, { Component, PropTypes } from 'react';

import EnhancedInput from '../../../components/enhanced-input';

import { Icon, Button } from 'antd';

class VisitingInfoItem extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      foldable: true,
      editable: false
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
    this.handleEditClick = this.handleEditClick.bind(this);
    this.handleAddClick = this.handleAddClick.bind(this);
    this.handleDeleteClick = this.handleDeleteClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleMoreClick = this.handleMoreClick.bind(this);
    this.handleFoldClick = this.handleFoldClick.bind(this);
    this.getFoldRender = this.getFoldRender.bind(this);
    this.getEditingRender = this.getEditingRender.bind(this);
  }

  handleMouseOver() {
    this.setState({
      visible: true
    });
  }

  handleMouseOut() {
    this.setState({
      visible: false
    });
  }

  handleEditClick() {
    this.setState({
      editable: true
    });
  }

  handleAddClick(value) {
    const { dataSource, itemInfo } = this.props;

    if (value.trim() !== '') {
      this.props.onSave({
        id: dataSource.id,
        fieldProp: itemInfo.dataIndex,
        fieldValue: value
      });
    }
  }

  handleDeleteClick(content, date) {
    const { dataSource, itemInfo } = this.props;

    this.props.onRemove(dataSource.id, itemInfo.dataIndex, content, date);
  }

  handleCancelClick() {
    this.setState({
      editable: false
    });
  }

  handleMoreClick(e) {
    e.preventDefault();
    this.setState({
      foldable: false
    });
  }

  handleFoldClick(e) {
    e.preventDefault();
    this.setState({
      foldable: true
    });
  }

  getFoldRender() {
    const { dataSource, itemInfo } = this.props,
          { editable } = this.state;

    if (dataSource[itemInfo.dataIndex].length > 1 && !editable) {
      if (this.state.foldable) {
        return (
          <a href="javascript: void(0);" onClick={this.handleMoreClick}>更多</a>
        );
      } else {
        return (
          <a href="javascript: void(0);" onClick={this.handleFoldClick}>收起</a>
        );
      }
    }

    return null;
  }

  getEditingRender() {
    const { visible, editable } = this.state;

    if (editable) {
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
           取消
          </Button>
        </div>
      );
    } else {
      return (
        <Icon
          type="edit"
          className={visible ? 'edit-icon-show' : 'edit-icon-hide'}
          onClick={this.handleEditClick}
        />
      );
    }
  }

  render() {
    const { dataSource, itemInfo } = this.props,
          { foldable, editable } = this.state,
          data = dataSource[itemInfo.dataIndex];

    return (
      <div
        className="cs-item-row"
        onMouseOver={this.handleMouseOver}
        onMouseOut={this.handleMouseOut}
        onDoubleClick={this.handleEditClick}
      >
        <label className="cs-item-row-label visiting-label">{itemInfo.title}</label>
        <div className="cs-item-row-content visiting-content">
          {data.length > 0 &&
            <ul>
              {data.map((item, index) => {
                return (
                  <li
                    key={item.date}
                    className={index > 0 && foldable && !editable ? 
                                  'visiting-item-hide' :
                                  'visiting-item'}
                  >
                    <span className="visiting-time">{item.date.split(' ')[0]}</span>
                    <span className="visiting-author">{item.author}</span>
                    <span className="visiting-detail">{item.content}</span>
                    {editable && 
                        <a
                          href="javascript: void(0);"
                          onClick={() => this.handleDeleteClick(item.content, item.date)}
                        >
                          删除
                        </a>
                    }
                  </li>
                );
              })}
            </ul>
          }
          <div className="visiting-opearator">
            {this.getFoldRender()}
            {this.getEditingRender()}
          </div>
        </div>
      </div>
    );
  }
}

VisitingInfoItem.defaultProps = {
  itemInfo: {},
  dataSource: {},
  onSave() {},
  onRemove() {}
};

VisitingInfoItem.propTypes = {
  itemInfo: PropTypes.object,
  dataSource: PropTypes.object,
  onSave: PropTypes.func,
  onRemove: PropTypes.func
};

export default VisitingInfoItem;
