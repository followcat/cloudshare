'use strict';
import React, { Component, PropTypes } from 'react';

import PreviewTopBarForm from './PreviewTopBarForm';

import {
  Form,
  Button,
  Icon
} from 'antd';

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
    const {
      prefixCls,
      currentPreview,
      prevText,
      nextText,
      total,
      origins
    } = this.props;

    return (
      <div className={`${prefixCls}`}>
        <Button
          type="primary"
          size="small"
          className={`${prefixCls}-prev`}
          disabled={currentPreview === 0}
          onClick={this.handlePrevClick}
        >
          <Icon type="left" />{prevText}
        </Button>
        <PreviewTopBarForm
          {...this.props}
        />
        <Button
          type="primary"
          size="small"
          className={`${prefixCls}-next`}
          disabled={currentPreview === total - 1}
          onClick={this.handleNextClick}
        >
          {nextText}<Icon type="right" />
        </Button>
      </div>
    );
  }
}

PreviewTopBar.defaultProps = {
  prefixCls: 'cs-preview-top-bar',
  currentPreview: 0,
  total: 0,
  prevText: 'Prev',
  nextText: 'Next'
};

PreviewTopBar.propTypes = {
  prefixCls: PropTypes.string,
  id: PropTypes.string,
  currentPreview: PropTypes.number,
  total: PropTypes.number,
  prevText: PropTypes.string,
  nextText: PropTypes.string,
  form: PropTypes.object,
  onPrevClick: PropTypes.func,
  onNextClick: PropTypes.func
};

export default PreviewTopBar = Form.create({})(PreviewTopBar);
