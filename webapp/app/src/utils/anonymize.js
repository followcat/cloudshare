'use strict';

const anonymizeGenerator = (name) => {
  const reg = /^([0-9]|[a-z]|[A-Z])+$/g;
  
  if (reg.test(name)) {
    return name;
  } else {
    return name.split('').map((item, index) => {
      if (index !== 0) {
        return '*';
      } else {
        return item;
      }
    }).join('');
  }
};

const anonymize = (legend) => {
  let newLegend = [];

  for (let i = 0, len = legend.length; i < len; i++) {
    let anonymizedName = anonymizeGenerator(legend[i]);
    if (newLegend.indexOf(anonymizedName) > -1) {
      anonymizedName += i;
    }

    newLegend.push(anonymizedName);
  }

  return newLegend;
};

export { anonymizeGenerator, anonymize };
