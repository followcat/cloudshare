'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon } from 'antd';

import HighLight from 'components/highlight';

import websiteText from 'config/website-text';

import { generateWorkExperience,
         parseExperience,
         parseEducation } from 'utils/summary-generator';

const language = websiteText.zhCN;

class ResumeTemplate extends Component {
  constructor() {
    super();
    this.combine = this.combine.bind(this);
    this.combines = this.combines.bind(this);
  }

  combine (current,gender,age,education,marital_status) {
   let a_current =  current || null,
    a_gender = gender || null,
    a_age = age || null,
    a_education = education || null,
    a_marital_status = marital_status || null,
    a_places = null,
    a = [];
    if(a_current) {
      a_places = a_current.places || null;
    } else {
      a_places = null;
    }
    a.push(a_places,a_gender,a_age,a_education,a_marital_status);
    a = a.filter(item => item!=undefined && item!==null);
    if(a.length == 0)
      return null
    else
      return a.filter(item => item!=undefined && item!==null);
  }

  combines (a) {
    if(typeof a == 'undefined') {
      return null
    }
    if(a.places || a.salary) {
      let places = a.places || null,
          salary = a.salary || null;
      if(places) {
        places = places.join(',');
      }
      if(salary) {
        if(salary.salary || salary.yearly) {
          salary  = salary.salary || salary.yearly
        } else {
          salary = null
        }
      }
      return [places,salary]
              .filter(item => item!=undefined && item!==null)
              .join('|')
    } else{
      return null
    }
  }
  render() {
    const { name, current, expectation, gender, age, education, marital_status,
            email, phone, experience, education_history, self_assessment
            } = this.props.dataSource
    const { highlight, searchText } = this.props;
    let c_current = this.combines(current),
        c_combine = this.combine(current,gender,age,education,marital_status),
        c_expectation = this.combines(expectation),
        c_education_history = parseEducation(education_history),
        c_experience = parseExperience(experience),
        highlightKW = searchText? highlight : null;
        console.log(highlightKW);
    return (
      <div className={`${this.props.prefixCls}-wrapper`}>
        <div className={`${this.props.prefixCls}`}>
          <div className={`${this.props.prefixCls}-info`}>
            <Icon type="user" style={{ fontSize:'25px'}}/>
            <h2>{name}</h2>
            <div className={`${this.props.prefixCls}-content`}>
              { c_combine?
              <p>{c_combine.join(" | ")}</p>
                : null
              }
              <p>
              { c_current?
              <span>{language.CURRENT}：{c_current}</span>
                : null
              }
              { c_expectation?
              <span>{language.EXPECTATION}：{c_expectation}</span>
                : null
              }
              </p>
              <div className='info-contact'>
                <Icon type="mail" /><span>{email||null}</span>
                <Icon type="mobile" /><span>{phone||null}</span>
              </div>
            </div>
            <div className={`${this.props.prefixCls}-hr`}>
              <hr />
            </div>
          </div>
          { c_education_history.length > 0?
          <div className={`${this.props.prefixCls}-education`}>
            <Icon type="edit" style={{ fontSize:'25px'}}/>
            <h2>{language.EDUCATION_HISTORY}</h2>
            <div className={`${this.props.prefixCls}-content`}>
                  {parseEducation(education_history).map((valueItem, index) => {
                    return (
                      <p key={index} className='education-item-title'>
                      {valueItem.map(item => {
                        return (
                          <span>{item}</span>
                          )
                      })}
                      </p>
                    );
                  })}
            </div>
            <div className={`${this.props.prefixCls}-hr`}>
              <hr />
            </div>
          </div>
          : null }
          { c_experience.length > 0?
          <div className={`${this.props.prefixCls}-position`}>
            <Icon type="tool" style={{ fontSize:'25px'}}/>
            <h2>{language.EXPERIENCE}</h2>
            <div className={`${this.props.prefixCls}-content`}>
                  {c_experience.reverse().map((valueItem, index) => {
                    return (
                      <div className='position-item'>
                      <p key={index} className='position-item-title'>
                        <span>{valueItem[0]}</span>
                        <span className='position-item-name'>
                          <strong>
                            <HighLight highlight={highlightKW}>
                              {valueItem[2]}
                            </HighLight>
                          </strong>
                        </span>
                        <span>
                        <strong>                            
                            <HighLight highlight={highlightKW}>
                              {valueItem[3]}
                            </HighLight>
                        </strong>
                        </span>
                      </p>
                      <p>{[valueItem[1],valueItem[4]].join('  |  ')}</p>
                      { (experience.position.length > 0 && 
                        typeof(experience.position[index].description) != 'undefined') ?
                        <div>
                          <p>{language.POSITION_DESCRIPTION}：</p>
                          <HighLight highlight={highlight}>
                            experience.position[index].description}
                          </HighLight>
                        </div>
                        : null
                      }
                      </div>
                    );
                  })}
            </div>
            <div className={`${this.props.prefixCls}-hr`}>
              <hr />
            </div>
          </div>
          : null }
          {experience.project?
          <div className={`${this.props.prefixCls}-project`}>
            <Icon type="folder" style={{ fontSize:'25px'}}/>
            <h2>{language.PROJECT_EXPERIENCE}</h2>
            <div className={`${this.props.prefixCls}-content`}>
                  {
                    experience.project.map((valueItem, index) => {
                    return (
                      <div className={`${this.props.prefixCls}-project-content`}>
                      <span>{valueItem.date_from} - {valueItem.date_to}</span>
                      <span className="project-company-name">
                        <strong>
                          <HighLight highlight={highlightKW}>
                            {valueItem.name}
                          </HighLight>
                        </strong>
                      </span>
                      { valueItem.company &&
                      <p>${language.FROM_COMPANY}：
                        <HighLight highlight={highlightKW}>
                          ${valueItem.company}
                        </HighLight>
                      </p>
                      }
                      { valueItem.description &&
                      <p>{language.PROJECT_DESCRIPTION}：
                      <div className="project-description">
                        <HighLight highlight={highlight}>
                          {valueItem.description}
                        </HighLight>
                      </div></p>
                      }
                      { valueItem.responsibility &&
                      <span>{language.RESPONSIBILITY_DESCRIPTION}：
                          <div className="project-description">
                            <HighLight highlight={highlight}>
                              {valueItem.responsibility}
                            </HighLight>
                          </div>
                        </span>
                      }
                      </div>
                    );
                    })
                  }
            </div>
            <div className={`${this.props.prefixCls}-hr`}>
              <hr />
            </div>
          </div>
          : null }
          {self_assessment &&
          <div className={`${this.props.prefixCls}-assessment`}>
            <Icon type="file-text" style={{ fontSize:'25px'}}/>
            <h2>{language.SELF_ASSESSMENT}</h2>
            <div className={`${this.props.prefixCls}-content`}>
                <HighLight highlight={highlight}>
                {self_assessment}
                </HighLight>
            </div>
            <div className={`${this.props.prefixCls}-hr`}>
              <hr />
            </div>
          </div>
          }
        </div>
      </div>
    );
  }
}

ResumeTemplate.defaultProps = {
  prefixCls: 'cs-resume-template',
  dataSource: null,
  html: '',
};

ResumeTemplate.propTypes = {
  prefixCls: PropTypes.string,
};

export default ResumeTemplate;
