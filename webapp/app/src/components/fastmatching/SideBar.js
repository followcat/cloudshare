'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon, Card, Form, Button, Tag, Modal } from 'antd';

import Competency from '../common/analyse/Competency';
import Experience from '../common/analyse/Experience';
import HistorySelection from '../common/analyse/HistorySelection';
import RadarChart from '../common/analyse/RadarChart';

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
    this.handleTagClose = this.handleTagClose.bind(this);
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

  handleTagClose(id, name) {
    this.props.onToggleSelection({
      id: id,
      name: name,
    });
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
            <Competency
              domId={chartsViewId}
              dataSource={this.props.dataSource}
            />
            <Experience 
              domId={chartsViewId}
              dataSource={this.props.dataSource}
            />
          </div>
          <div className="radar">
            <div className="title">
              <h3>Draw Charts</h3>
            </div>
            <HistorySelection
              selection={this.props.selection}
              onToggleSelection={this.props.onToggleSelection}
            />
            <RadarChart 
              selection={this.props.selection}
              postData={this.props.postData}
            />
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
                      afterClose={() => this.handleTagClose(item.get('id'), item.get('name'))}
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

SideBar.propTypes = {
  visible: PropTypes.bool,
  dataSource: PropTypes.array,
  selection: PropTypes.array,
  postData: PropTypes.object,
  onToggleSelection: PropTypes.func,
}