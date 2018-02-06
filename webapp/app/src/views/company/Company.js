'use strict';
import React, { Component } from 'react';
import { browserHistory } from 'react-router';

import { Layout } from 'views/layout';

import Summary from 'components/summary';

import {
  Tabs,
  Tag,
  Spin,
  Row,
  Col,
  message,
  Card
} from 'antd';

import {
  getResumeCompanyInfo,
  getSimilar
} from 'request/company';

import { API } from 'API';
import { URL } from 'URL';

import { generateSummary } from 'utils/summary-generator';
import History from 'utils/history';
import StorageUtil from 'utils/storage';

class Company extends Component {
  constructor() {
    super();
    this.state = {
      uniqueId: '',
      companyId: '',
      name: '', 
      product: '',
      website: '',
      employees: '',
      type: '',
      address: '',
      conumber: '',
      district: '',
      email: '',
      introduction: '',
      project: [],
      collected: false,
      panelLoading: false,
      confirmLoading: false,
      similar: []
    };
  }

  componentWillMount() {
    const id = this.props.params.companyId;
    this.setState({
      companyId: id
    });
    this.getCompanyDataSource(id);
  }

  getCompanyDataSource(id) {
    this.setState({
      panelLoading: true
    });

    getResumeCompanyInfo({
      id: id
    }, json => {
      if (Object.keys(json > 0)) {
        const { name, project, total_employees,
          type, website, place, conumber, district, email, description } = json.data;
        this.setState({
          companyId: id,
          name: name,
          website: website,
          employees: total_employees,
          type: type,
          address: place,
          project: project,
          introduction: description
        });
      }
    });
  }

  render() {
    const {
      companyId,
      name, 
      product,
      website,
      employees,
      type,
      address,
      project,
      conumber,
      district,
      email,
      introduction,
    } = this.state;
    console.log(project);
    return (
      <Layout>
        <div className="cs-layout-company">
            <Card title={name}>
            {employees && <Tag>{employees}</Tag>}
            {type && <Tag>{type}</Tag>}
            <div className="company-content">
              <h2>公司介绍</h2>
              <Card>
              <div className="company-content-text">
                <p>{introduction}</p>
              </div>
              </Card>
            </div>
            <div className="company-project-text">
              <h2>公司项目</h2>
                { project.map(item =>{
                  return (
                    <Card>
                  <Row type="flex" justify="center" align="middle" className="company-project-text-row">
                    <Col span={11}>
                    <span>{item.date_from}-{item.date_to}</span>
                    </Col>
                    <Col span={11}>
                    <span>{item.name}</span>
                    </Col>
                    <Col span={22}>
                    <p>{item.description}</p>
                    </Col>
                  </Row>
                  </Card>
                  )
                  })
                }
            </div>
            </Card>
          <div className="company-side">
          </div>
        </div>
      </Layout>
    );
  }
}

export default Company;
