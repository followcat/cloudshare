'use strict';
import React, { Component, PropTypes } from 'react';

import EnhancedInput from 'components/enhanced-input';

import {
  Col,
  Input,
  Button,
  Tag
} from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class Cell extends Component {
  constructor() {
    super();
    this.state = {
      fieldProp: '',
      fieldValue: null,
      editStatus: false,
      openable: false
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleDoubleClick = this.handleDoubleClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSaveClick = this.handleSaveClick.bind(this);
    this.handleEnhancedInputClick = this.handleEnhancedInputClick.bind(this);
    this.handleAfterClose = this.handleAfterClose.bind(this);
    this.getArrayDOMNormalRender = this.getArrayDOMNormalRender.bind(this);
    this.getArrayDOMEditingRender = this.getArrayDOMEditingRender.bind(this);
    this.getArrayDOMRender = this.getArrayDOMRender.bind(this);
    this.getStringDOMRender = this.getStringDOMRender.bind(this);
  }

  handleClick() {
    this.setState({
      openable: !this.state.openable
    });
  }

  handleDoubleClick() {
    const { dataSource, dataIndex } = this.props;

    this.setState({
      editStatus: true,
      fieldProp: dataIndex,
      fieldValue: dataSource[dataIndex] instanceof Array ? dataSource[dataIndex].content : dataSource[dataIndex]
    });
  }

  handleCancelClick() {
    this.setState({
      editStatus: false
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

  handleEnhancedInputClick(fieldValue) {
    const { dataSource, dataIndex } = this.props;

    if (fieldValue.trim() !== '') {
      this.props.onSave({
        id: dataSource.id,
        fieldProp: dataIndex,
        fieldValue: fieldValue
      });

      this.setState({
        editStatus: false
      });
    }
  }

  handleAfterClose(content, date) {
    const { dataSource, dataIndex } = this.props;

    this.props.onRemove(dataSource.id, dataIndex, content, date);

    this.setState({
      editStatus: false
    });
  }

  getArrayDOMNormalRender() {
    const { dataSource, dataIndex } = this.props,
          { openable, editStatus } = this.state;
    
    let text = '';

    dataSource[dataIndex].forEach((item, index) => {
      if (index === dataSource[dataIndex].length - 1) {
        text += item.content;
      } else {
        text += `${item.content}, `;
      }
    });

    return (
      <div
        className={openable && !editStatus ? '' : 'ommit'}
        title={text}
        onClick={this.handleOmmitClik}
      >
        {text || '无'}
      </div>
    );
  }

  getArrayDOMEditingRender() {
    const { dataSource, dataIndex } = this.props;
    return (
      <div>
        {dataSource[dataIndex].map((item, index) => {
           return (
            <Tag
              key={index}
              closable={true}
              onClose={() => this.handleAfterClose(item.content, item.date)}
            >
              {item.content}
            </Tag>
          );
        })}
        <div className="cs-additional-input-group extra-opearator">
          <EnhancedInput
            type="plus"
            placeholder=""
            size="small"
            resettable={true}
            style={{ display: 'inline-block', width: '80%' }}
            onClick={this.handleEnhancedInputClick}
          />
          <Button
            size="small"
            type="ghost"
            onClick={this.handleCancelClick}
          >
            {language.CANCEL}
          </Button>
        </div>
      </div>
    );
  }

  getArrayDOMRender() {
    const { editable } = this.props,
          { editStatus } = this.state;

    if (editable) {
      if (editStatus) {
        return this.getArrayDOMEditingRender();
      } else {
        return this.getArrayDOMNormalRender();
      }
    } else {
      return this.getArrayDOMNormalRender();
    }
  }

  getStringDOMRender() {
    const { dataSource, dataIndex, editable } = this.props,
          { editStatus, openable, fieldValue } = this.state;

    const cellCls = openable && !editStatus ? '' : 'ommit';

    if (editable) {
      return (
        <div className={cellCls}>
          {!editStatus ?
            dataSource[dataIndex] || '无' :
            <div className="cs-item-row-content">
              <div className="cs-input-group">
                <Input
                  value={fieldValue}
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
    } else {
      return (
        <div className={cellCls}>{dataSource[dataIndex] || '无'}</div>
      );
    }
  }

  render() {
    const { dataSource, dataIndex, width } = this.props;
    return (
      <div
        style={{ width: width }}
        className="cell-item"
        onClick={this.handleClick}
        onDoubleClick={this.handleDoubleClick}
      >
        {dataSource[dataIndex] instanceof Array ?
          this.getArrayDOMRender() :
          this.getStringDOMRender()
        }
      </div>
    );
  }
}

Cell.defaultProps = {
  editable: true,
  width: '87%',
  onSave() {},
  onRemove() {}
};

Cell.propTypes = {
  editable: PropTypes.bool,
  width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  dataIndex: PropTypes.string,
  dataSource: PropTypes.object,
  onSave: PropTypes.func,
  onRemove: PropTypes.func
};

export default Cell;
