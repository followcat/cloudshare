'use strict';
import React, { Component, PropTypes } from 'react';

import TablePlus from 'components/table-plus';
import Charts from 'components/analyse-charts/Charts';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

import {
  Modal,
  Button,
  Collapse,
  Input,
  Spin,
  Checkbox,
  message
} from 'antd';

import { getValuableData } from 'request/analyse';
import { getJobDescriptionSearch } from 'request/jobdescription';

import { getRadarOption } from 'utils/chart_option';


class DrawChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      jdId: null,
      jdDoc: '',
      type: 'id',
      dataSource: [],
      selectedRowKeys: [],
      radarOption: {},
      visible: false,
      chartVisible: false,
      anonymized: false,
      spinning: false
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleCollapseChange = this.handleCollapseChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleAnonymousChange = this.handleAnonymousChange.bind(this);
    this.handleOk = this.handleOk.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleRowSelectionChange = this.handleRowSelectionChange.bind(this);
    this.handlePaginationChange = this.handlePaginationChange.bind(this);
    this.handleRowSelectionSelect = this.handleRowSelectionSelect.bind(this);
  }

  handleClick() {
    getJobDescriptionSearch({
      current_page: 1,
      page_size: 9999,
      search_items: [["status", "Opening"]]
    },json => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          dataSource: typeof(this.state.jdId) == 'string'? 
            json.data.filter(item => item.id === this.props.jdId) : json.data
        });
      }
    });
  }

  handleOk() {
    this.setState({
      visible: false,
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  handleCollapseChange(e) {
    this.setState({
      type: e
    });
  }

  handleInputChange(event) {
    this.setState({
      jdDoc: event.target.value,
    });
  }

  handleSubmit() {
    const { type, jdId, jdDoc, anonymized } = this.state,
          { resumeId } = this.props;
    if (jdId === '' && jdDoc === '') {
      message.error('请选择一个职位描述.');
      return;
    }

    let requestParams = type === 'id' ? { id: jdId } : { doc: jdDoc };

    this.setState({
      chartVisible: true,
      spinning: true
    });

    getValuableData(Object.assign(requestParams, {
      name_list: [`${resumeId}`]
    }), (json) => {
      if (json.code === 200) {
        const option = getRadarOption(json.data.max, json.data.result, anonymized);
        this.setState({
          spinning: false,
          radarOption: option
        });
      }
    });
  }

  handleAnonymousChange(e) {
    this.setState({
      anonymized: e.target.checked,
    });
  }

  handleRowSelectionChange(selectedRowKeys, selectedRows) {
    this.setState({
      selectedRowKeys: selectedRowKeys,
    });
  }

  handlePaginationChange() {
    this.setState({
      selectedRowKeys: [],
      jdId: '',
    });
  }

  handleRowSelectionSelect(record, selected, selectedRows) {
    this.setState({
      jdId: record.id,
    });
  }

  componentWillReceiveProps(nextProps) {
   this.setState({
     visible: nextProps.visible,
     jdId: nextProps.jdId
   },() => {
    if (this.props.visible)
      this.handleClick();
    if (typeof(this.props.jdId) == 'string')
      this.handleSubmit();
   });
  }

  getExpandedRowRender(record) {
    return (
      <div>
        <div>
          {record.description.split('\n').map((item, index) => { return (<p key={index}>{item}</p>); })}
        </div>
      </div>
    );
  }

  render() {
    const { dataSource, radarOption, spinning, chartVisible } = this.state;
    const columns = [
      {
        title: '公司名称',
        dataIndex: 'company_name',
        key: 'company_name',
        width: '20%',
      }, {
        title: '职位',
        dataIndex: 'name',
        key: 'position',
        width: '25%',
      }, {
        title: '创建人',
        dataIndex: 'committer',
        key: 'creator',
        width: '15%',
      },{
      title: language.CURRENT_STATUS,
      dataIndex: 'status',
      key: 'status',
      width: '15%',
      render: (text) => {
        return text === 'Opening' ? 
            <span style={{ color: 'green' }}>{language.OPENING}</span> :
            <span style={{ color: 'red' }}>{language.CLOSED}</span>;
      }
    },
    , {
      title: language.OPERATION,
      key: 'operation',
      width: '15%',
      render: (record) => (
        <a onClick={() => {
          this.setState({jdId:record.id,type: 'id'},() => this.handleSubmit());
          }}>{language.MATCH_ACTION}</a>
      )
    }
    ];

    const rowSelection = {
      type: 'radio',
      selectedRowKeys: this.state.selectedRowKeys,
      onChange: this.handleRowSelectionChange,
      onSelect: this.handleRowSelectionSelect,
    };

    const pagination = {
      total: dataSource.length,
      pageSize: 5,
      size: 'small',
      onChange: this.handlePaginationChange
    };

    const chartWrapperStyle = {
      width: '100%',
      height: 460,
      marginTop: 10,
    };

    return (
      <div style={{  marginLeft: 4 }}>
        <Modal
          title="雷达图"
          visible={this.state.visible}
          style={{ top: 12 }}
          width={980}
          onOk={this.handleOk}
          onCancel={this.handleCancel}
        >
          <Collapse
            accordion
            defaultActiveKey="id"
            onChange={this.handleCollapseChange}
          >
            <Collapse.Panel
              header={'职位描述列表'}
              key="id"
            >
              <TablePlus
                isToolbarShowed={true}
                isSearched={true}
                columns={columns}
                loading={spinning}
                dataSource={dataSource}
                pagination={pagination}
                size="small"
                rowKey={record => record.id}
                expandedRowRender={record => this.getExpandedRowRender(record)}
              />
            </Collapse.Panel>
            <Collapse.Panel
              header={'职位描述内容'}
              key="doc"
            >
              <Input
                type="textarea"
                rows="4"
                onChange={this.handleInputChange}
              />
            </Collapse.Panel>
          </Collapse>
          <Button
            type="ghost"
            style={{ marginTop: 4 }}
            onClick={this.handleSubmit}
          >
            提交
          </Button>
          <Checkbox
            style={{ marginLeft: 8 }}
            onChange={this.handleAnonymousChange}
          >
            匿名
          </Checkbox>
          <Spin spinning={spinning}>
            <div style={Object.assign(chartWrapperStyle, { display: chartVisible ? 'block' : 'none' })}>
              {Object.keys(radarOption).length > 0 ?
                <Charts
                  option={radarOption}
                  style={chartWrapperStyle}
                />
               : ''}
             </div>
          </Spin>
        </Modal>
      </div>
    );
  }
}

DrawChart.propTypes = {
  resumeId: PropTypes.string,
};

export default DrawChart;
