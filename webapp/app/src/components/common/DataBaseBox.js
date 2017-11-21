'use strict';
import React, { Component } from 'react';

import Storage from 'utils/storage';
import Generator from 'utils/generator';
import 'whatwg-fetch';
import 'databasebox.less';

export default class DataBaseBox extends Component {

  constructor() {
    super();
    this.state = {
      dbList: [],
      visible: false,
    };
    this.loadDB = this.loadDB.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.renderList = this.renderList.bind(this);
  }

  loadDB() {
    fetch(`/api/dbnumbers`, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${Storage.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData()
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          dbList: json.data,
        });
      }
    })
  }

  handleClick() {
    if (this.state.visible) {
      this.setState({
        visible: false,
      });
    } else {
      this.setState({
        visible: true,
      });
    }
  }

  renderList() {
    const dbList = this.state.dbList,
          _pj = Storage.get('_pj'),
          arr = [];
    for (let key in dbList) {
      if (key === _pj) {
        arr.unshift(<li key={key}>{`${key}: ${dbList[key]}`}</li>)
      } else {
        arr.push(<li key={key}>{`${key}: ${dbList[key]}`}</li>);
      }
    }
    return arr;
  }

  componentDidMount() {
    this.loadDB();
  }

  render() {
    const listClass = this.state.visible ? 'count-list showed' : 'count-list hidden',
          totalClass = this.state.visible ? 'total' : 'total radius';
    return (
      <div className="count-box">
        <ul className={listClass}>
          {this.renderList()}
        </ul>
        <div
          className={totalClass}
          onClick={this.handleClick}
        >
          {`Total: ${this.state.dbList['total']}`}
        </div>
      </div>
    );
  }
}