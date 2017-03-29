'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Input,
  Tag
} from 'antd';

class Cell extends Component {
  constructor(props) {
    super(props);
    
    const { dataSource, dataIndex } = props;

    this.state = {
      fieldValue: dataSource[dataIndex] instanceof Array ? '' : dataSource[dataIndex],
      editStatus: false,
      openable: false
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleAfterClose = this.handleAfterClose.bind(this);
    this.getArrayDOMNormalRender = this.getArrayDOMNormalRender.bind(this);
    this.getArrayDOMEditingRender = this.getArrayDOMEditingRender.bind(this);
    this.getArrayDOMRender = this.getArrayDOMRender.bind(this);
    this.getStringDOMRender = this.getStringDOMRender.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    const { editStatus, dataSource, dataIndex } = nextProps;

    if (editStatus === false) {
      this.setState({
        fieldValue: dataSource[dataIndex] instanceof Array ? '' : dataSource[dataIndex]
      });
    }
  }

  handleClick() {
    this.setState({
      openable: !this.state.openable
    });
  }

  handleChange(e) {
    const { dataIndex } = this.props;

    this.setState({
      fieldValue: e.target.value
    });

    this.props.onUpdateFieldValues(dataIndex, { content: e.target.value });
  }

  handleAfterClose(item) {
    const { dataIndex } = this.props;

    this.props.onUpdateDeleteList(dataIndex, item);
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
    const { dataSource, dataIndex } = this.props,
          { fieldValue } = this.state;

    return (
      <div>
        {dataSource[dataIndex].map((item, index) => {
           return (
            <Tag
              key={index}
              closable={true}
              onClose={() => this.handleAfterClose(item)}
            >
              {item.content}
            </Tag>
          );
        })}
        <div className="cs-additional-input-group extra-opearator">
          <Input value={fieldValue} size="small" onChange={this.handleChange} />
        </div>
      </div>
    );
  }

  getArrayDOMRender() {
    const { editable, editStatus } = this.props;
          // { editStatus } = this.state;

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

  /**
   * 当dataSource数据类型为string的渲染函数
   * 
   * @returns 
   * 
   * @memberOf Cell
   */
  getStringDOMRender() {
    const {
            itemInfo,
            dataSource,
            dataIndex,
            editable,
            editStatus 
          } = this.props,
          { openable, fieldValue } = this.state;

    const cellCls = openable && !editStatus ? '' : 'ommit';

    let type = 'text';

    if (itemInfo && itemInfo.type) {
      type = itemInfo.type;
    }

    if (editable) {   // 允许编辑
      return (
        <div className={cellCls}>
          {!editStatus ?
            dataSource[dataIndex] || '无' :
            <div className="cs-item-row-content">
              <div className="cs-input-group">
                <Input
                  value={fieldValue}
                  size="small"
                  type={type}
                  onChange={this.handleChange}
                />
              </div>
            </div>
          }
        </div>
      );
    } else {    // 不允许编辑
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
  width: '87%'
};

Cell.propTypes = {
  editable: PropTypes.bool,
  editStatus: PropTypes.bool,
  width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  itemInfo: PropTypes.object,
  dataIndex: PropTypes.string,
  dataSource: PropTypes.object,
  onUpdateFieldValues: PropTypes.func,
  onUpdateDeleteList: PropTypes.func
};

export default Cell;
