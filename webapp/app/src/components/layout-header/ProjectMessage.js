'use strict';
import React, { Component } from 'react';

class ProjectMessage extends Component {
  render() {
    return (
      <div className="cs-header-project">
        <span>{this.props.project}</span>
      </div>
    );
  }
}

export default ProjectMessage;
