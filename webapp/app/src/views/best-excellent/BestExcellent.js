'use strict';
import moment from 'moment';
import React, { Component } from 'react';

import { API } from 'API';
import { Row, Col, Table, Radio, DatePicker } from 'antd';
import ColorGrad from 'utils/color-grad';
import { getFastMatching } from 'request/fastmatching';

class BestExcellent extends Component {
  constructor() {
    super();
    const date = new Date();
    this.state = {
      dataSource: [],
      date: moment(date).add(0, 'days'),
      numbers: "1",
      dateFormat: 'YYYY-MM-DD',
      pagesize: '20',
      loading: true,
      fromcache: true,
      allJDAPI: API.LSI_BY_ALL_JD_API,
    };
    this.handleDateChange = this.handleDateChange.bind(this);
    this.handleNumbersChange = this.handleNumbersChange.bind(this);
    this.getAllJDDataSource = this.getAllJDDataSource.bind(this);
  }

  componentDidMount() {
    this.getAllJDDataSource();
  }

  getAllJDDataSource() {
    const { fromcache, allJDAPI, dateFormat, date, numbers } = this.state;
    const colorGrad = new ColorGrad();
    const gradient = colorGrad.gradient();
    const defFilterData = { date: [moment(date).add(-1, 'days').format(dateFormat),
                                   date.format(dateFormat)] };
    var postData = { filterdict: defFilterData, threshold: 0.78,
                     fromcache: fromcache, numbers: parseInt(numbers) };
    this.setState({
      loading: true,
    });
    getFastMatching(allJDAPI, postData, json => {
      if (json.code === 200) {
        json.data.forEach((value) => {
          value.color = gradient[parseInt(value.CVvalue*100)];
        });
        this.setState({
          dataSource: json.data,
          loading: false,
        });
      }
    });
  }

  handleDateChange(e) {
    this.setState({ date: moment(e) }, this.getAllJDDataSource);
  }

  handleNumbersChange(e) {
    this.setState({ numbers: e.target.value }, this.getAllJDDataSource);
  }

  render() {
    const {
      dataSource,
      loading,
      pagesize,
      date,
      dateFormat,
      numbers
    } = this.state;
    const columns = [{
      title: '公司',
      key: 'JDcompany',
      render: (text, record) => (
        <a href={ `/fastmatching?jd_id=${record.JDid}&init_append_commentary=true` }
           target="_blank">
          { record.JDcompany } 
        </a>
      )
    }, {
      title: '职位',
      dataIndex: 'JDname',
      key: 'JDname',
    },{
      title: '候选人资料',
      key: 'CVid',
      render: (text, record) => (
        <a href={`/resume/${record.id}`} target="_blank"
           style={ { color: record.color } }>
          { record.id } | { record.name } | { record.company } | { record.position } 
        </a>
      ),
    },{
      title: '来源',
      dataIndex: 'origin',
      key: 'CVorigin',
    } ];
    return (
      <div>
        <Row gutter={16}>
          <Col span={5} />
          <Col span={2}>
            <span>
              选择日期
            </span>
          </Col>
          <Col span={5}>
              <DatePicker defaultValue={date} format={dateFormat} onChange={this.handleDateChange}/>
          </Col>
          <Col span={2}>
            <span>
              选择显示人数
            </span>
          </Col>
          <Col span={5}>
            <Radio.Group defaultValue={numbers} onChange={this.handleNumbersChange}>
              <Radio.Button value="1">1</Radio.Button>
              <Radio.Button value="2">2</Radio.Button>
              <Radio.Button value="3">3</Radio.Button>
            </Radio.Group>
          </Col>
          <Col span={5} />
        </Row>
        <Table columns={columns}
               dataSource={dataSource}
               size={pagesize}
               loading={loading} />
      </div>
    );
  }
}

export default BestExcellent;