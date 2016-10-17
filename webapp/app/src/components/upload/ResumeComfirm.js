'use strict';
import React, { Component, PropTypes } from 'react';

import { Button } from 'antd';

export default class ResumeComfirm extends Component {
  
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Button
        loading={this.props.loading}
        onClick={this.props.onClick}
      >
        Comfirm
      </Button>
    );
  }
}

ResumeComfirm.propTypes = {
  id: PropTypes.string,
  loading: PropTypes.bool,
};