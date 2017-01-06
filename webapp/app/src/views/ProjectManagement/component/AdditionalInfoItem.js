'use strict';
import React, { Component, PropTypes } from 'react';

import EnhancedInput from '../../../components/enhanced-input';

import { Icon, Tag, Button } from 'antd';

import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;

class AdditionalInfoItem extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      editable: false,
      opening: false
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleEnhancedInputClick = this.handleEnhancedInputClick.bind(this);
    this.handleAfterClose = this.handleAfterClose.bind(this);
    this.handleOmmitClik = this.handleOmmitClik.bind(this);
    this.getNormalRender = this.getNormalRender.bind(this);
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

  handleClick() {
    this.setState({
      editable: true
    });
  }

  handleCancel() {
    this.setState({
      editable: false
    });
  }

  handleEnhancedInputClick(fieldValue) {
    const { dataSource, itemInfo } = this.props;

    if (fieldValue.trim() !== '') {
      this.props.onSave({
        id: dataSource.id,
        fieldProp: itemInfo.dataIndex,
        fieldValue: fieldValue
      });
    }
  }

  handleAfterClose(content, date) {
    const { dataSource, itemInfo } = this.props;

    this.props.onRemove(dataSource.id, itemInfo.dataIndex, content, date);
  }

  handleOmmitClik() {
    const opening = this.state.opening;

    this.setState({
      opening: !opening
    });
  }

  getNormalRender(dataSource, dataIndex) {
    let textContent = '';
    
    dataSource[dataIndex].forEach((item, index) => {
      if (index === dataSource[dataIndex].length - 1) {
        textContent += item.content;
      } else {
        textContent += `${item.content}, `;
      }
    });

    return (
      <div>
        <span
          className={this.state.opening ? 'cs-item-row-content-text' : 'cs-item-row-content-text ommit'}
          title={textContent}
          onClick={this.handleOmmitClik}
        >
          {textContent}
        </span>
        <Icon
          type="edit"
          className={this.state.visible ? 'edit-icon-show' : 'edit-icon-hide'}
          onClick={this.handleClick}
        />
      </div>
    );
  }

  getEditingRender(dataSource, dataIndex) {
    return (
      <div>
        {dataSource[dataIndex].map((item, index) => {
          return (
            <Tag
              key={index}
              closable={true}
              afterClose={() => this.handleAfterClose(item.content, item.date)}
            >
              {item.content}
            </Tag>
          );
        })}
        <div className="cs-additional-input-group">
          <EnhancedInput
            type="plus"
            placeholder=""
            size="small"
            resettable={true}
            onClick={this.handleEnhancedInputClick}
          />
          <Button
            size="small"
            type="ghost"
            onClick={this.handleCancel}
          >
            {language.CANCEL}
          </Button>
        </div>
        
      </div>
    );
    
  }

  render() {
    const { itemInfo, dataSource } = this.props;

    return (
      <div
        className="cs-item-row"
        onMouseOver={this.handleMouseOver}
        onMouseOut={this.handleMouseOut}
        onDoubleClick={this.handleClick}
      >
        <label className="cs-item-row-label">{itemInfo.title}</label>
        <div className="cs-item-row-content">
          {this.state.editable ?
              this.getEditingRender(dataSource, itemInfo.dataIndex) :
              this.getNormalRender(dataSource, itemInfo.dataIndex)
          }
        </div>
      </div>
    );
  }
}

AdditionalInfoItem.defaultProps = {
  dataSource: {},
  itemInfo: {},
  onSave() {},
  onRemove() {}
};

AdditionalInfoItem.propTypes = {
  dataSource: PropTypes.object,
  itemInfo: PropTypes.object,
  onSave: PropTypes.func,
  onRemove: PropTypes.func
};

export default AdditionalInfoItem;
