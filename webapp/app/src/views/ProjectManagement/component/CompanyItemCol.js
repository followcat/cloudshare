'use strict';
import React, { Component, PropTypes } from 'react';

import { Col, Input, Button } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class CompanyItemCol extends Component {
  constructor() {
    super();
    this.state = {
      fieldProp: '',
      fieldValue: '',
      editStatus: false,
      opening: false
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleDoubleClick = this.handleDoubleClick.bind(this);
    this.handleSaveClick = this.handleSaveClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
  }

  handleClick() {
    this.setState({
      opening: !this.state.opening
    });
  }
  
  handleDoubleClick() {
    const { dataSource, dataIndex } = this.props;

    this.setState({
      editStatus: true,
      fieldProp: dataIndex,
      fieldValue: dataSource[dataIndex]
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

  handleChange(e) {
    this.setState({
      fieldValue: e.target.value
    });
  }

  render() {
    const { dataSource, dataIndex, span } = this.props,
          { editStatus, opening } = this.state;

    const itemCellCls = opening ? 'company-item-cell' : 'company-item-cell ommit';

    return (
      <Col span={span}>
        <div
          className={itemCellCls}
          onClick={this.handleClick}
          onDoubleClick={this.handleDoubleClick}
        >
          {!editStatus ?
            dataSource[dataIndex] || '无' :
            <div className="cs-item-row-content">
              <div className="cs-input-group">
                <Input
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
      </Col>
    );
  }
}

CompanyItemCol.propTypes = {
  dataSource: PropTypes.object,
  span: PropTypes.string,
  dataIndex: PropTypes.string,
  onSave: PropTypes.func
};

export default CompanyItemCol;
