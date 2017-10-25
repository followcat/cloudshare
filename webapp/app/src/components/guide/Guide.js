'use strict';
import React, { Component, PropTypes } from 'react';

import { browserHistory } from 'react-router';

import StorageUtil from 'utils/storage';

import classNames from 'classnames';

import { Steps, Icon, Checkbox } from 'antd';
const Step = Steps.Step;

class Guide extends Component {
  constructor() {
    super();
    this.state ={
      guideStatus: 0,
    };
    this.UploadClick = this.UploadClick.bind(this);
    this.CustomerClick = this.CustomerClick.bind(this);
    this.MathingClick = this.MathingClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    if(e.target.checked){
      StorageUtil.set('guideStatus',false);
      this.setState({
        guideStatus : false
      })
    } else {
      StorageUtil.set('guideStatus',0);
    }
  }

  UploadClick() {
    StorageUtil.set('guideStatus',1);
    browserHistory.push({
      pathname: 'uploader',
      query: { guide: true }
    });
  }

  CustomerClick() {
    StorageUtil.set('guideStatus',2);
    browserHistory.push('/pm/company/list?guide=true');
  }

  MathingClick() {
    StorageUtil.set('guideStatus',3);
    browserHistory.push('/fastmatching?guide=true');
  }

  componentWillMount() {
    const status = StorageUtil.get('guideStatus');
    this.setState({
      guideStatus : status
    });
  }

  componentDidMount() {
  }

  render() {
    const { props, prefixCls } = this.props;
    const {guideStatus} = this.state;
    const classSet = classNames({
      [`${prefixCls}`]: true,
      'hidden': guideStatus == 'false',
      'show' : guideStatus == true
    });
    return (
      <div className={classSet}>
        <Steps  direction="vertical" current={guideStatus} >
          <Step title="简历上传" ref="step1" description="可以批量上传简历" onClick={this.UploadClick}/>
          <Step title="新建客户" description="完美跟踪一条龙服务" onClick={this.CustomerClick}/>
          <Step title="匹配" description="新建职位后进行匹配， 精确查找候选人" onClick={this.MathingClick}/>
        </Steps>
        <div className={`${prefixCls}-nohint`}>
          <label>
            <Checkbox onChange={this.handleChange}>不再提示</Checkbox>
          </label>
        </div>
      </div>
    );
  }
}

Guide.defaultProps = {
  prefixCls: 'cs-guide',
  title: '',
};

Guide.propTypes = {
  prefixCls: PropTypes.string,
  type: PropTypes.string,
  title: PropTypes.string,
};

export default Guide;
