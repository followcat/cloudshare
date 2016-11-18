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
  if (nextProps) {
    return nextProps.location.pathname.split('/')[1] || props.route.indexRoute.name;
  } else {
    return props.location.pathname.split('/')[1] || props.route.indexRoute.name;
  }
};
