'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon, Input, Button } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class BasicInfoItem extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      fieldProp: '',
      fieldValue: '',
      editStatus: false,
      opening: false
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSaveClick = this.handleSaveClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleOmmitClik = this.handleOmmitClik.bind(this);
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
    const { itemInfo, dataSource } = this.props;

    this.setState({
      editStatus: true,
      fieldProp: itemInfo.dataIndex,
      fieldValue: dataSource[itemInfo.dataIndex]
    });
  }

  handleChange(e) {
    this.setState({
      fieldValue: e.target.value
    });
  }

  handleSaveClick() {
    const { dataSource } = this.props,
          { fieldProp, fieldValue } = this.state;

    if (fieldValue.trim() !== '') {
      this.props.onSave({ id: dataSource.id, fieldProp: fieldProp, fieldValue: fieldValue });
    }

    this.setState({
      editStatus: false
    });
  }

  handleCancelClick() {
    this.setState({
      editStatus: false
    });
  }

  handleOmmitClik() {
    const opening = this.state.opening;

    this.setState({
      opening: !opening
    });
  }

  render() {
    const { itemInfo, labelCls, contentCls, dataSource } = this.props;
    
    return (
      <div
        className="cs-item-row"
        onMouseOver={this.handleMouseOver}
        onMouseOut={this.handleMouseOut}
        onDoubleClick={this.handleClick}
      >
        <label className={`cs-item-row-label ${labelCls}`}>{itemInfo.title}</label>
        {!this.state.editStatus ?
            <div className={`cs-item-row-content ${contentCls}`}>
              <span
                className={this.state.opening ? 'cs-item-row-content-text' : 'cs-item-row-content-text ommit'}
                title={dataSource[itemInfo.dataIndex]}
                onClick={this.handleOmmitClik}
              >
                {itemInfo.render ?
                    itemInfo.render(dataSource[itemInfo.dataIndex]) :
                    dataSource[itemInfo.dataIndex]
                }
              </span>
              <Icon
                type="edit"
                className={this.state.visible ? 'edit-icon-show' : 'edit-icon-hide'}
                onClick={this.handleClick}
              />
            </div> :
            <div className="cs-item-row-content">
              <div className="cs-input-group">
                <Input
                  type={itemInfo.type || 'text'}
                  value={this.state.fieldValue}
                  size="small"
                  onChange={this.handleChange}
                />
                <div className="cs-button-group">
                  <Button
                    type="primary"
                    size="small"
                    onClick={this.handleSaveClick}
                  >
                    {language.SAVE}
                  </Button>
                  <Button
                    size="small"
                    onClick={this.handleCancelClick}
                  >
                    {language.CANCEL}
                  </Button>
                </div>
              </div>
            </div>
        }
      </div>
    );
  }
}

BasicInfoItem.defaultProps = {
  labelCls: '',
  contentCls: '',
  itemInfo: {},
  dataSource: {},
  onSave() {}
};

BasicInfoItem.propTypes = {
  labelCls: PropTypes.string,
  contentCls: PropTypes.string,
  itemInfo: PropTypes.object,
  dataSource: PropTypes.object,
  onSave: PropTypes.func
};

export default BasicInfoItem;
