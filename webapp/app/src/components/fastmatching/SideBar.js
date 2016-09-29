'use strict';
import React, { Component } from 'react';

import { Icon, Card, Form, Button, Tag, Modal } from 'antd';

import Competency from '../common/analyse/Competency';

import classNames from 'classnames';

function getStyle(obj) {
  return obj.currentStyle ? obj.currentStyle : window.getComputedStyle(obj, null);
}

let timer = null;

function moved(element, t, target) {
  clearInterval(timer);

  timer = setInterval(() => {
    let right = parseInt(getStyle(element).right),
        speed = (target - right)/5;

    speed = speed > 0 ? Math.ceil(speed) : Math.floor(speed);

    if (right === target) {
      clearInterval(timer);
    } else {
      element.style.right = right + speed + 'px';
    }
  }, t);
}

export default class SideBar extends Component {

  constructor(props) {
    super(props);
    this.state = {
      visible: false,
    };
    this.handleSidebarBtnClick = this.handleSidebarBtnClick.bind(this);
  }

  handleSidebarBtnClick() {
    const visible = this.state.visible;

    let t = 50,
        target = visible ? -200 : 0,
        element = document.getElementById('sidebar');

    if (visible) {
      this.setState({
        visible: false,
      });
    } else {
      this.setState({
        visible: true,
      });
    }
    moved(element, t, target);
  }

  shouldComponentUpdate(nextProps, nextState) {
    return nextProps.selection.id === this.props.id;
  }

  render() {
    const chartsViewId = 'chartsView';

    const classSet = classNames({
      'sidebar': true,
      'showed': this.props.visible === true,
      'hidden': this.props.visible === false,
    });
    return (
      <div className={classSet} id="sidebar">
        <div className="sidebar-button" onClick={this.handleSidebarBtnClick}>
          {this.state.visible ? <Icon type="caret-right" /> : <Icon type="caret-left" />}
        </div>
        <Card className="sidebar-container">
          <div className="analyse">
            <div className="title">
              <h3>Analyse</h3>
            </div>
            <Button type="primary">Show Competency</Button>
            <Button type="primary">Show Work Experience</Button>
          </div>
          <div className="radar">
            <div className="title">
              <h3>Draw Charts</h3>
            </div>
            <Button type="primary">Select From History</Button>
            <Button type="primary">Show Radar Chart</Button>
            <div className="selection-box">
              <div className="selection-title">
                <h4>Selection</h4>
              </div>
              <div className="selection-container">
                {this.props.selection.map((item, index) => {
                  return (
                    <Tag
                      key={index}
                      closable={true}
                      data-id={item.get('id')}
                    >
                      {item.get('name') ? item.get('name') : item.get('id')}
                    </Tag>
                  );
                })}
              </div>
            </div>
          </div>
        </Card>
      </div>
    );
  }
}