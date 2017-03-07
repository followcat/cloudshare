'use strict';
import React, { Component, PropTypes } from 'react';
import {
  Card,
  Row,
  Col,
  Form,
  Input
} from 'antd';

class DetailInformation extends Component {
  constructor() {
    super();
    this.state = {
      editing: false,
    };
    this.handleEditClick = this.handleEditClick.bind(this);
    this.handleSaveClick = this.handleSaveClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.renderValue = this.renderValue.bind(this);
    this.renderForm = this.renderForm.bind(this);
    this.renderExtra = this.renderExtra.bind(this);
  }

  handleEditClick(e) {
    e.preventDefault();
    this.setState({
      editing: true,
    });
  }

  handleSaveClick(e) {
    e.preventDefault();
    this.setState({
      editing: false,
    });
    const value = this.props.form.getFieldsValue();
    this.props.onSave(value);
  }

  handleCancelClick(e) {
    e.preventDefault();
    this.setState({
      editing: false,
    });
  }

  renderValue(v) {
    const record = this.props.dataSource[v.dataIndex] || '';

    if (v.render) {
      return v.render(record);
    } else {
      return record;
    }
  }

  renderForm(v) {
    const { getFieldProps } = this.props.form,
          record = this.props.dataSource[v.dataIndex] || '',
          type = v.type || 'text';

    return (
      <Input
        {...getFieldProps(v.dataIndex, { initialValue: record })}
        type={type}
      />
    );
  }

  renderExtra() {
    const {
      editable,
      saveText,
      cancelText,
      editText,
    } = this.props;
    let extra = null;

    if (editable) {
      if (this.state.editing) {
        extra = (
          <div className="cs-editing">
            <a href="#" onClick={this.handleSaveClick}>{saveText}</a>
            <a href="#" onClick={this.handleCancelClick}>{cancelText}</a>
          </div>
        );
      } else {
        extra = (
          <a href="#" onClick={this.handleEditClick}>{editText}</a>
        );
      }
    }

    return extra;
  }

  render() {
    const { title, rows } = this.props,
          { editing } = this.state;
    
    return (
      <Card
        loading={false}
        title={title}
        extra={this.renderExtra()}
        className={this.props.prefixCls}
      >
        {rows.map(v => {
          return (
            <Row key={v.key} className="cs-item-row">
              <Col span={4}>{v.title}</Col>
              <Col span={18}>
                {editing && v.editable ? this.renderForm(v) : this.renderValue(v)}
              </Col>
            </Row>
          );
        })}
      </Card>
    );
  }
}

DetailInformation.defaultProps = {
  prefixCls: 'cs-details-card',
  title: '',
  rows: [],
  dataSource: {},
  editable: false,
  saveText: 'Save',
  cancelText: 'Cancel',
  editText: 'Edit',
  onSave() {}
};

DetailInformation.propTypes = {
  title: PropTypes.string,
  rows: PropTypes.array,
  dataSource: PropTypes.object,
  editable: PropTypes.bool,
  saveText: PropTypes.string,
  cancelText: PropTypes.string,
  editText: PropTypes.string,
  onSave: PropTypes.func,
};

export default DetailInformation = Form.create({})(DetailInformation);
