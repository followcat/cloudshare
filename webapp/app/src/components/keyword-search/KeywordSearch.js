'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col, Input, Button } from 'antd';

class KeywordSearch extends Component {
  constructor() {
    super();
    this.state = {
      value: ''
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  componentWillMount() {
    const { defaultValue } = this.props;

    if (defaultValue) {
      this.setState({
        value: defaultValue
      });
    }
  }

  handleChange(e) {
    this.setState({
      value: e.target.value
    });
  }

  handleClick() {
    const { value } = this.state;
    
      this.props.onSearch(value);
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.handleClick();
    }
  }

  getHorizontalRender() {
    const { btnText, defaultText } = this.props,
          { value } = this.state;

    return (
      <div>
        <Row>
          <Col span={24}>
            <Input
              value={value}
              size="large"
              placeholder={defaultText}
              onChange={this.handleChange}
              onKeyPress={this.handleKeyPress}
            />
          </Col>
        </Row>
        <Row>
          <Col span={6} offset={9}>
            <Button
              type="primary"
              size="large"
              onClick={this.handleClick}
            >
              {btnText}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }

  getInlineRender() {
    const { btnText, defaultText} = this.props,
          { value } = this.state;

    return (
      <Row>
        <Col span={19}>
          <Input
            value={value}
            placeholder={defaultText}
            size="large"
            onChange={this.handleChange}
            onKeyPress={this.handleKeyPress}
          />
        </Col>
        <Col span={4} offset={1}>
          <Button
            type="primary"
            size="large"
            onClick={this.handleClick}
          >
            {btnText}
          </Button>
        </Col>
      </Row>
    );
  }
  render() {
    const { prefixCls, horizontal, inline } = this.props;

    return (
      <div className={prefixCls}>
        {inline && this.getInlineRender() || horizontal && this.getHorizontalRender()}
      </div>
    );
  }
}

KeywordSearch.defaultProps = {
  prefixCls: 'cs-keyword-search',
  defaultText: "在关键字前后添加双引号,可进行精确搜索",
  btnText: 'Search',
  horizontal: false,
  inline: false,
  onSearch() {}
};

KeywordSearch.propTypes = {
  prefixCls: PropTypes.string,
  defaultValue: PropTypes.string,
  btnText: PropTypes.string,
  horizontal: PropTypes.bool,
  inline: PropTypes.bool,
  form: PropTypes.object,
  getFieldProps: PropTypes.func,
  onSearch: PropTypes.func
};

export default KeywordSearch;
