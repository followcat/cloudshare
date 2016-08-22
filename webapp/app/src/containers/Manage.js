'use strict';
import React, { Component, PropTypes } from 'react';
import 'whatwg-fetch';

import Header from '../components/manage/Header';
import MainWrapper from '../components/manage/MainWrapper';

import config from '../../config';


export default class Manage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datas: [],
      visible: false,
      confirmLoading: false,
    };

    this.handleModalOpen = this.handleModalOpen.bind(this);
    this.handleModalClose = this.handleModalClose.bind(this);
    this.handleSubmitCreation = this.handleSubmitCreation.bind(this);
  }

  loadUserList() {
    fetch(config.host + '/api/accounts')
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        let datas = json.data.map((value, index) => {
          return { key: index, name: value };
        });
        this.setState({ datas: datas });
      }
    })
  }

  handleModalOpen() {
    this.setState({
      visible: true,
    });
  }

  handleModalClose() {
    this.setState({
      visible: false,
    });
  }

  handleSubmitCreation(user) {
    this.setState({
      confirmLoading: true,
    });
    fetch(config.host + '/api/accounts',{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        name: user.name,
        password: user.password,
      })
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        let datas = this.state.datas,
            len = datas.length;
        datas.push({ key: len, name: user.name });
        this.setState({
          datas: datas,
          confirmLoading: false,
          visible: false,
        });
      }
    });
  }

  componentDidMount() {
    this.loadUserList();
  }

  render() {
    return (
      <div>
        <div id="viewport">
          <Header />
          <MainWrapper 
            userList={this.state.datas}
            visible={this.state.visible}
            confirmLoading={this.state.confirmLoading}
            onSubmitCreation={this.handleSubmitCreation}
            onModalOpen={this.handleModalOpen}
            onModalClose={this.handleModalClose}
          />
        </div>
      </div>
    );
  }
}