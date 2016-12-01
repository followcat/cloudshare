'use strict';
import React, { Component, PropTypes } from 'react';
import AlertPrompt from '../alert-prompt';
import { URL } from '../../config/url';

class VersionPrompt extends Component {
  render() {
    return (
      <div>
      {this.props.dataSource.length ?
          <AlertPrompt
            type="info"
            title="Information: "
          >
            <span>There may be same resume content </span>
            {this.props.dataSource.map((id, index) => {
              return (
                <a
                  key={id}
                  href={URL.getResumeURL(id)}
                  target="_blank"
                  style={{ marginLeft: 8 }}
                >
                  {`Version ${index+1}: ${id}`}
                </a>
              );
            })}
          </AlertPrompt> :
          null
      }
      </div>
    );
  }
}

VersionPrompt.defaultProps = {
  dataSource: [],
};

VersionPrompt.propTypes = {
  dataSource: PropTypes.array,
};

export default VersionPrompt;
