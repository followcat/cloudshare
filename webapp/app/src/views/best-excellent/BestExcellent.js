'use strict';
import moment from 'moment';
import React, { Component } from 'react';

import { API } from 'API';
import { Table } from 'antd';
import ColorGrad from 'utils/color-grad';
import { getFastMatching } from 'request/fastmatching';

class BestExcellent extends Component {
  constructor() {
    super();
    this.state = {
      dataSource: [],
      pagesize: '20',
      loading: true,
      fromcache: true,
      allJDAPI: API.LSI_BY_ALL_JD_API,
    };
  }

  componentDidMount() {
    const { fromcache, allJDAPI } = this.state;
    const date = new Date();
    const colorGrad = new ColorGrad();
    const gradient = colorGrad.gradient();
    const defFilterData = { date: [moment(date).add(-1, 'days').format('YYYY-MM-DD'),
                                   moment(date).add(0, 'days').format('YYYY-MM-DD')] };
    var postData = { filterdict: defFilterData, threshold: 0.75, fromcache: fromcache };
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

  render() {
    const {
      dataSource,
      loading,
      pagesize,
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
        <Table columns={columns}
               dataSource={dataSource}
               size={pagesize}
               loading={loading} />
      </div>
    );
  }
}

export default BestExcellent;