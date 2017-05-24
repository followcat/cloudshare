'use strict';
import React from 'react';
import ReactDOM from 'react-dom';

import { AppContainer } from 'react-hot-loader';

import rootContainer from 'views/rootContainer';

const render = (Component) => {
  ReactDOM.render(
    <AppContainer>
      <Component />
    </AppContainer>,
    document.getElementById('root')
  );
};

render(rootContainer);

if (module.hot) {
  module.hot.accept('views/rootContainer', () => {
    render(rootContainer);
  });
}
