'use strict';
import React, { Component, PropTypes } from 'react';

class FilterInfo extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const style = this.props.visible ? { display: 'block' } : { display: 'none' };
    return (
      <div style={style}>
        <p>总共有<em>{this.props.total}</em>相关结果。</p>
      </div>
    );
  }
}

FilterInfo.propTypes = {
  visible: PropTypes.bool,
  total: PropTypes.number,
};

export default FilterInfo;
