'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon, Card } from 'antd';

import Competency from 'components/analyse-charts/Competency';
import Experience from 'components/analyse-charts/Experience';
import HistorySelection from 'components/analyse-charts/HistorySelection';
import RadarChart from 'components/analyse-charts/RadarChart';
import Tag from 'components/tag';

import getStyle from 'utils/get-style';

import classNames from 'classnames';

let timer = null;

function moved(element, t, target) {
  clearInterval(timer);

  timer = setInterval(() => {
    let right = parseInt(getStyle(element, 'right')),
        speed = (target - right)/5;

    speed = speed > 0 ? Math.ceil(speed) : Math.floor(speed);

    if (right === target) {
      clearInterval(timer);
    } else {
      element.style.right = right + speed + 'px';
    }
  }, t);
}

class SiderBar extends Component {
  constructor() {
    super();
    this.state = {
      panelVisible: false
    };
    this.handleSiderbarBtnClick = this.handleSiderbarBtnClick.bind(this);
    this.handleTagClose = this.handleTagClose.bind(this);
    this.renderSelectionDOM = this.renderSelectionDOM.bind(this);
  }

  handleSiderbarBtnClick() {
    const { panelVisible } = this.state;
    let t = 50,
        target = panelVisible ? -200 : 0,
        element = this.refs.siderbar;
    
    this.setState({
      panelVisible: !panelVisible
    });

    moved(element, t, target);
  }

  handleTagClose(id, name) {
    this.props.onToggleSelection({
      id: id,
      name: name,
    });
  }

  renderSelectionDOM() {
    let dom = this.props.selection.map((item, index) => {
      return (
        <Tag
          key={index}
          text={item.get('name') ? item.get('name') : item.get('id')}
          onClick={() => this.handleTagClose(item.get('id'), item.get('name'))}
        />
      );
    });
    return dom;
  }

  render() {
    const {
            visible,
            closable,
            dataSource,
            postData,
            selection
          } = this.props,
          { panelVisible } = this.state,
          chartsViewId = 'chartsView';

    const classSet = classNames({
      'siderbar': true,
      'showed': visible,
      'hidden': !visible,
    });

    if (closable) {
      return null;
    } else {
      return (
        <div className={classSet} ref="siderbar">
          <div className="siderbar-button" onClick={this.handleSiderbarBtnClick}>
            {panelVisible ? <Icon type="caret-right" /> : <Icon type="caret-left" />}
          </div>
          <Card className="siderbar-container">
            <div className="analyse">
              <div className="title">
                <h3>分析</h3>
              </div>
              <Competency
                domId={chartsViewId}
                dataSource={dataSource}
              />
              <Experience
                domId={chartsViewId}
                dataSource={dataSource}
              />
            </div>
            <div className="radar">
              <div className="title">
                <h3>雷达图</h3>
              </div>
              <HistorySelection
                selection={selection}
                onToggleSelection={this.props.onToggleSelection}
              />
              <RadarChart 
                selection={selection}
                postData={postData}
              />
              <div className="selection-box">
                <div className="selection-title">
                  <h4>选中候选人列表</h4>
                </div>
                <div className="selection-container">
                  {this.renderSelectionDOM()}
                </div>
              </div>
            </div>
          </Card>
        </div>
      );
    }
  }
}

SiderBar.propTypes = {
  visible: PropTypes.bool,
  closable: PropTypes.bool,
  dataSource: PropTypes.array,
  selection: PropTypes.array,
  postData: PropTypes.object,
  onToggleSelection: PropTypes.func,
};

export default SiderBar;
