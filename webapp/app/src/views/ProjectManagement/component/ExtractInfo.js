'use strict';
import React, { Component, PropTypes } from 'react';
import EnhancedInput from '../../../components/enhanced-input';
import {
  Row,
  Col,
  Card,
  Form,
  Input,
  Button,
  Tag
} from 'antd';
import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;
const FormItem = Form.Item;

const isValueNotNull = (object) => {
  let notNull = true;
  for (let k in object) {
    if (object[k] === 'undefined' || object[k] === '' || object[k] === null) {
      notNull = false;
      return notNull;
    }
  }
  return notNull;
};

class ExtractInfo extends Component {
  constructor() {
    super();
    this.state = {
      editing: false,
    };
    this.handleEditClick = this.handleEditClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleEnhancedInputClick = this.handleEnhancedInputClick.bind(this);
    this.handleAfterClose = this.handleAfterClose.bind(this);
    this.getExtractElement = this.getExtractElement.bind(this);
    this.getNormalRender = this.getNormalRender.bind(this);
    this.getEditingRender = this.getEditingRender.bind(this);
  }

  handleEditClick() {
    this.setState({
      editing: true,
    });
  }

  handleCancelClick() {
    this.setState({
      editing: false,
    });
  }

  handleEnhancedInputClick(feildValue) {
    if (feildValue instanceof Object && this.props.onCreate && isValueNotNull(feildValue)) {
      this.props.onCreate(feildValue);
    }
  }

  handleAfterClose(key, value, date) {
    this.props.onRemove(key, value, date);
  }

  getExtractElement() {
    const { editable } = this.props;
    let extractElement = null;

    if (editable) {
      if (this.state.editing) {
        extractElement = (<a href="javascript: void(0);" onClick={this.handleCancelClick}>{language.CANCEL}</a>);
      } else {
        extractElement = (<a href="javascript: void(0);" onClick={this.handleEditClick}>{language.EDIT}</a>);
      }
    }

    return extractElement;
  }

  getNormalRender(prop) {
    if (Array.isArray(prop)) {
      return prop.map(v => {
        return <span key={v.content} className="cs-extra-item">{v.content}</span>
      });
    }
    return null;
  }

  getEditingRender(dataIndex, prop) {
    if (Array.isArray(prop)) {
      return prop.map((v, i) => {
        return (
          <Tag
            key={i}
            closable={this.state.editing}
            afterClose={() => this.handleAfterClose(dataIndex, v.content, v.date)}
          >
            {v.content}
          </Tag>
        );
      });
    }
    return null;
  }

  render() {
    const { dataSource } = this.props;

    const rows = [{
      title: language.OPEN_POSITION,
      dataIndex: 'position',
    }, {
      title: language.CONTACT,
      dataIndex: 'clientcontact',
    }, {
      title: language.CONTACT_WAY,
      dataIndex: 'updatednumber',
    }, {
      title: language.RELATED_COMPANY,
      dataIndex: 'relatedcompany',
    }];

    return (
      <Card
        title={this.props.title}
        style={{ marginBottom: 16 }}
        extra={this.getExtractElement()}
      >
        {rows.map((item, index) => {
          return (
            <Row key={index} className="cs-extra-row">
              <Col span={4}>{item.title}</Col>
              <Col span={16}>
                {this.state.editing ?
                    this.getEditingRender(item.dataIndex, dataSource[item.dataIndex]) :
                    this.getNormalRender(dataSource[item.dataIndex])
                }
              </Col>
              {this.state.editing ? 
                  (
                    <Col span={4}>
                      <EnhancedInput
                        type="plus"
                        placeholder=""
                        dataIndex={item.dataIndex}
                        onClick={this.handleEnhancedInputClick}
                      />
                    </Col>
                  ) :
                  null
              }
            </Row>
          );
        })}
      </Card>
    );
  }
}

ExtractInfo.default = {
  editable: true,
};

ExtractInfo.propTypes = {
  editable: PropTypes.bool,
};

export default ExtractInfo;
