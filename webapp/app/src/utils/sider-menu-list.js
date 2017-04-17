'use strict';

export const getMenu = (childRoutes) => {
  return childRoutes.map((item) => {
    return {
      key: item.name,
      url: item.path,
      text: item.title,
    };
  });
};

export const getCurrentActive = (props, nextProps=null) => {
  let path;

  if (nextProps) {
    path = nextProps.location.pathname.split('/');
  } else {
    path = props.location.pathname.split('/');
  }

  return path[path.length - 1] || props.route.indexRoute.name;
};
