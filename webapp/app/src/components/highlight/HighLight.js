import React, { Component, PropTypes } from 'react';
import { Row, Col } from 'antd';

import classNames from 'classnames';

import ColorGrad from 'utils/color-grad';

class HighLight extends Component {
  render() {
    const {
      children,
      prefixCls,
      dataSource,
      highlight,
      position
    } = this.props;
    const colorGrad = new ColorGrad()
    const gradient = colorGrad.gradient();
  let value = children;
  highlight && Object.keys(highlight).map((item) =>{
    let Color = gradient ? gradient[parseInt(highlight[item]*100)] : {};
    let invalue = '<span class="cs-highlight-item"'+'style="font-weight: bolder;'+
    'padding: 3px 2px 1px;'+
    'border-radius: 5px;'+
    'background-color:'+Color+'">'+item+'</span>',
          items = item.replace(/\+|\-|\\|\/|\*\[|\|/g,"\\$&"),  
          regex = new RegExp(items, "i");
          value = value.replace(regex,invalue);
  });
    return (
      <pre className={prefixCls} dangerouslySetInnerHTML={{__html: value}}>
      </pre>
    );
  }
}

HighLight.defaultProps = {
  prefixCls: 'cs-highlight',
  highlight: [],
  position: 'center'
};

HighLight.propTypes = {
  children: PropTypes.string,
  prefixCls: PropTypes.string,
  dataSource: PropTypes.array,
  position: PropTypes.string
};

export default HighLight;
