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
    
    if (value.trim()) {
      this.props.onSearch(value);
    }
  }

  getHorizontalRender() {
    const { btnText } = this.props,
          { value } = this.state;

    return (
      <div>
        <Row>
          <Col span={24}>
            <Input
              value={value}
              size="large"
              onChange={this.handleChange}
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
    const { btnText } = this.props,
          { value } = this.state;

    return (
      <Row>
        <Col span={19}>
          <Input
            value={value}
            size="large"
            onChange={this.handleChange}
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
