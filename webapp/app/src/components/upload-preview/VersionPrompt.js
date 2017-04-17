'use strict';
import React, { Component, PropTypes } from 'react';

import AlertPrompt from 'components/alert-prompt';

import { URL } from 'config/url';

class VersionPrompt extends Component {
  render() {
    const {
      title,
      message,
      dataSource
    } = this.props;

    return (
      <div>
        {dataSource.length > 0 ?
          <AlertPrompt type="info" title={title}>
            <span>{message}</span>
            {dataSource.map((id, index) => {
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
  title: 'Informations',
  message: 'There may be same resume content ',
  dataSource: []
};

VersionPrompt.propTypes = {
  title: PropTypes.string,
  message: PropTypes.string,
  dataSource: PropTypes.array
};

export default VersionPrompt;
