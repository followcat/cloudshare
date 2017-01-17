'use strict';
import findIndex from 'lodash/findIndex';

const generateWorkExperience = (experience) => {
  if (typeof experience !== 'undefined') {
    let company = experience.company || [],
        position = experience.position || [];

    if (position.length > 0) {
      for (let i = 0, len = position.length; i < len; i++) {
        let id = position[i].at_company,
            index = findIndex(company, ['id', id]);
        
        if (index > -1) {
          position[i] = Object.assign({}, position[i], {
            companyName: company[index].name,
            business: company[index].business || null
          });
        }
      }
      return position;
    } else {
      return company;
    }
  }

  return [];
};

/*
 * summary组件数据结构: [{ name: ,value: }]
 * label为summary组件渲染的name, 按顺序依次渲染
 */
const label = [
  'name',
  'email',
  'gender',
  'phone',
  'age',
  'education',
  'marital_status',
  'school',
  'position',
  'company',
  'experience',
  'education_history',
];

const getCompanyNameById = (id, companyList) => {
  for (let i = 0, len = companyList.length; i < len; i++) {
    if (id === companyList[i].id) {
      return companyList[i].name;
    }
  }
  return '';
};

const parseExperience = (experience) => {
  let value = [],
      expArray = generateWorkExperience(experience);

  for (let i = expArray.length - 1; i >= 0; i--) {
    let workTime = `${expArray[i].date_from} - ${expArray[i].date_to}`,
        business = expArray[i].business || null,
        positionName = expArray[i].name || null,
        companyName = expArray[i].companyName || expexpArrayerience.name || null,
        duration = expArray[i].duration;

    value.push([workTime, business, positionName, companyName, duration]);
  }
  
  return value;
};

const parseEducation = (education) => {
  let value = [];

  if (typeof education !== 'undefined') {
    for (let i = 0, len = education.length; i < len; i++) {
      let educationTime = `${education[i].date_from} - ${education[i].date_to}`,
          degree = education[i].education,
          major = education[i].major,
          school = education[i].school;

      value.push([educationTime, degree, major, school]);
    }
  }

  return value;
};

const generateSummary = (dataSource) => {
  let result = [];

  for (let i = 0, len = label.length; i < len; i++) {
    if (label[i] in dataSource) {
      let obj = {};
      obj.name = label[i];

      if (label[i] === 'experience') {  // 特殊处理: 解析experience, 生成数组, 赋值给value
        obj.value = parseExperience(dataSource[label[i]]);
      } else if (label[i] === 'education_history') {  // 特殊处理: 解析education_history, 生成数组, 赋值给value
        obj.value = parseEducation(dataSource[label[i]]);
      } else {  // 一般情况, 直接赋值
        obj.value = dataSource[label[i]];
      }

      result.push(obj);
    } else {
      result.push({
        name: label[i],
        value: '',
      });
    }
  }

  return result;
}

module.exports = {
  generateSummary,
  generateWorkExperience
};