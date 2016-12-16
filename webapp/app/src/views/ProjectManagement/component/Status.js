'use strict';
import React, { Component, PropTypes } from 'react';
import { Select } from 'antd';
const Option = Select.Option;

class Status extends Component {
  render() {
    const props = this.props;

    return (
      <div
        className="cs-status-selection"
        style={props.style}
      >
        <label className="cs-status-selection-label">{props.statusLabel}</label>
        <Select
          defaultValue={props.defaultValue}
          style={{ width: props.width }}
          onChange={props.onChange}
        >
          {props.dataSource.map(item => {
            return (
              <Option
                key={item.text}
                value={item.value}
              >
                {item.text}
              </Option>
            );
          })}
        </Select>
      </div>
    );
  }
}

Status.defaultProps = {
  dataSource: [],
  statusLabel: ''
};

Status.propTypes = {
  style: PropTypes.object,
  statusLabel: PropTypes.string,
  dataSource: PropTypes.arrayOf(PropTypes.shape({
    text: PropTypes.string,
    value: PropTypes.string,
  })),
};

export default Status;
