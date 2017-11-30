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
      visible: true,
    };
    this.UploadClick = this.UploadClick.bind(this);
    this.CustomerClick = this.CustomerClick.bind(this);
    this.MathingClick = this.MathingClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.CloseClick = this.CloseClick.bind(this);
  }

  handleChange(e) {
    if(e.target.checked){
      StorageUtil.set('guideStatus',false);
      this.setState({
        guideStatus : true
      })
    } else {
      StorageUtil.set('guideStatus',0);
    }
  }

  CloseClick() {
    this.setState({
      visible : false
    });
  }

  UploadClick() {
    StorageUtil.set('guideStatus',1);
    if(global.ismember)
    browserHistory.push({
        pathname: 'uploader',
        query: { guide: true }
    });
    else
      browserHistory.push({
        pathname: 'prouploader',
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
    const { props, prefixCls, } = this.props;
    const {guideStatus, visible} = this.state;
    const classSet = classNames({
      [`${prefixCls}`]: true,
      'hidden': !visible || guideStatus == 'false',
      'show' :  visible || guideStatus == true
    });
    return (
      <div className={classSet}>
        <div className={`${prefixCls}-close`}  onClick={this.CloseClick}>
        <Icon type="close" />
        </div>
        <Steps  direction="vertical" current={guideStatus} >
          { global.ismember ?
          <Step title="简历上传" ref="step1" description="可以批量上传简历" onClick={this.UploadClick}/>
          :
          <Step title="简历上传" ref="step1" description="可以上传个人简历" onClick={this.UploadClick}/>
          }
          <Step title="客户管理" description="跟踪管理客户状态" onClick={this.CustomerClick}/>
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
