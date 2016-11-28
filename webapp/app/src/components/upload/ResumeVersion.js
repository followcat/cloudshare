'use strict';
import React, { Component, PropTypes } from 'react';
import AlertPrompt from '../alert-prompt';
import { URL } from '../../request/api';

class ResumeVersion extends Component {
  render() {
    return (
      <div>
      {this.props.dataSource.length ?
        <AlertPrompt 
          type="warning"
          title="Warning: "
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

ResumeVersion.defaultProps = {
  dataSource: [],
};

ResumeVersion.propTypes = {
  dataSource: PropTypes.array,
};

export default ResumeVersion;
