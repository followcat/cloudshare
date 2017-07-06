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
      daterange: [moment(date).add(-1, 'days'), moment(date).add(0, 'days')],
      numbers: "3",
      dateFormat: 'YYYY-MM-DD',
      pagesize: '20',
      loading: true,
      fromcache: true,
      allJDAPI: API.LSI_BY_ALL_JD_API,
    };
    this.disabledDate = this.disabledDate.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.handleNumbersChange = this.handleNumbersChange.bind(this);
    this.getAllJDDataSource = this.getAllJDDataSource.bind(this);
    this.getExpandedRowRender = this.getExpandedRowRender.bind(this);
  }

  componentDidMount() {
    this.getAllJDDataSource();
  }

  getAllJDDataSource() {
    const { fromcache, allJDAPI, dateFormat, daterange, numbers } = this.state;
    const colorGrad = new ColorGrad();
    const gradient = colorGrad.gradient();
    const defFilterData = { date: [daterange[0].format(dateFormat),
                                   daterange[1].format(dateFormat)] };
    var postData = { filterdict: defFilterData, threshold: 0.78,
                     fromcache: fromcache, numbers: parseInt(numbers) };
    this.setState({
      loading: true,
    });
    getFastMatching(allJDAPI, postData, json => {
      if (json.code === 200) {
        json.data.forEach((JDid) => {
          JDid.CV.forEach((item) => {
            item.color = gradient[parseInt(item.CVvalue*100)];
          });
        });
        this.setState({
          dataSource: json.data,
          loading: false,
        });
      }
    });
  }

  handleDateChange(dates) {
    this.setState({ daterange: dates }, this.getAllJDDataSource);
  }

  handleNumbersChange(e) {
    this.setState({ numbers: e.target.value }, this.getAllJDDataSource);
  }

  disabledDate(current) {
    return current.valueOf() > Date.now() || current.valueOf() < Date.now()-14*24*60*60*1000;
  }

  getExpandedRowRender(record) {
    return (
      <div>
      {
        record.description
      }
      </div>
    );
  };

  render() {
    const {
      dataSource,
      loading,
      pagesize,
      daterange,
      dateFormat,
      numbers
    } = this.state;

    const columns = [
      {
        title: '公司职位',
        key: 'name',
        width: 300,
        render: (text, record) => (
          <a href={ `/fastmatching?jd_id=${record.ID}&init_append_commentary=true` }
             target="_blank">
            { record.company } | { record.name }
          </a>
        )
      }, {
        title: '人选',
        key: 'CV',
        render: (text, record) => (
          <div>
          {
            record.CV.map((item) => {
              return (
                <Row gutter={16}>
                  <Col span={16}>
                    <a href={`/resume/${item.id}`} target="_blank"
                     style={ { color: item.color } }>
                    { item.id } | { item.name } | { item.company } | { item.position } | { item.school }
                    </a>
                  </Col>
                  <Col span={8}>
                    <span>{ item.origin }</span>
                  </Col>
                </Row>
              );
            })
          }
          </div>
        )
      }
    ];

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
              <DatePicker.RangePicker
               defaultValue={daterange}
               disabledDate={this.disabledDate}
               onChange={this.handleDateChange}/>
          </Col>
          <Col span={2}>
            <span>
              选择显示人数
            </span>
          </Col>
          <Col span={5}>
            <Radio.Group defaultValue={numbers} onChange={this.handleNumbersChange}>
              <Radio.Button value="1">1</Radio.Button>
              <Radio.Button value="3">3</Radio.Button>
              <Radio.Button value="5">5</Radio.Button>
              <Radio.Button value="10">10</Radio.Button>
            </Radio.Group>
          </Col>
          <Col span={5} />
        </Row>
        {dataSource && dataSource.length 
          ?    <Table columns={columns}
               dataSource={dataSource}
               defaultExpandAllRows={true}
               rowKey={record => record.JDid}
               expandedRowRender={record => this.getExpandedRowRender(record)}
               size={pagesize}
               loading={loading} />
          : '暂无数据' }
      </div>
    );
  }
}

export default BestExcellent;