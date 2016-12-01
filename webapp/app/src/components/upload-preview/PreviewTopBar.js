'use strict';
import React, { Component, PropTypes } from 'react';
import { Row, Col, Form, Input, Select, Button, Icon } from 'antd';
const FormItem = Form.Item,
      Option = Select.Option;

class PreviewTopBar extends Component {
  constructor() {
    super();
    this.handlePrevClick = this.handlePrevClick.bind(this);
    this.handleNextClick = this.handleNextClick.bind(this);
  }

  handlePrevClick(e) {
    e.preventDefault();
    const fieldsValue = this.props.form.getFieldsValue();
    this.props.onPrevClick({
      id: this.props.id,
      fieldsValue: fieldsValue
    });
  }

  handleNextClick(e) {
    e.preventDefault();
    const fieldsValue = this.props.form.getFieldsValue();
    this.props.onNextClick({
      id: this.props.id,
      fieldsValue: fieldsValue
    });
  }

  render() {
    const props = this.props;

    return (
      <div className={`${props.prefixCls}`}>
        <Button
          type="primary"
          size="small"
          className={`${props.prefixCls}-prev`}
          disabled={props.currentPreview === 0}
          onClick={this.handlePrevClick}
        >
          <Icon type="left" />Prev
        </Button>
        {props.children}
        <Button
          type="primary"
          size="small"
          className={`${props.prefixCls}-next`}
          disabled={props.currentPreview === props.total - 1}
          onClick={this.handleNextClick}
        >
          Next<Icon type="right" />
        </Button>
      </div>
    );
  }
}

PreviewTopBar.defaultProps = {
  prefixCls: 'cs-preview-top-bar',
  currentPreview: 0,
  total: 0,
};

PreviewTopBar.propTypes = {
  prefixCls: PropTypes.string,
  currentPreview: PropTypes.number,
  total: PropTypes.number,
};

export default PreviewTopBar;
