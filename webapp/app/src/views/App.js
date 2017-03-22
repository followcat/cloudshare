'use strict';
import React, { Component, PropTypes } from 'react';

class App extends Component {
  render() {
    return (
      <div id="app">
        {this.props.children}
      </div>
    );
  }
}

App.propTypes = {
  children: PropTypes.element
};

export default App;
