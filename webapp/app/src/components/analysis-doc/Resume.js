'usr strict';
import React, { Component, PropTypes } from 'react';

import { generateSummary } from 'utils/summary-generator';

//import './css/bootstrap.css';
//import './css/dashboard.css';
//import './css/style.css';

class Resume extends Component {

  constructor(props) {
    super(props);

    this.getSummaryObject = this.getSummaryObject.bind(this);
  }

  getSummaryObject(summaryList) {
    let SummaryObject = {};
    for (let i = 0, len = summaryList.length; i < len; i++) {
      SummaryObject[summaryList[i].name] = summaryList[i].value;
    }
    return SummaryObject;
  }

  render() {
    const summaryList = generateSummary(this.props.dataSource);
    const props = this.getSummaryObject(summaryList);
    console.log(props);

    let workExperience = [],
        companyList = [],
        educationExperience = props.education_history ? props.education_history : [];

    if (props.experience) {
      workExperience = props.experience.hasOwnProperty('position') ? props.experience.position : [],
      companyList = props.experience.hasOwnProperty('company') ? props.experience.company : [];
    }

    return (

<div>
<div className="col-sm-3 col-md-2 sidebar">
    <div className="sidebar_top">
       <h1>候选人</h1> 
    </div>
    <div className="details">
       <h3>职位</h3>
       <p>{props.position}</p>
       <h3>公司</h3>
       <p>{props.company}</p>
       <h3>毕业院校</h3>
       <p>{props.school}</p>
       <h3>文化程度</h3>
       <p>{props.education}</p>
       <h3>年龄</h3>
       <p>{props.age}</p>
       <h3>性别</h3>
       <p>{props.gender}</p>
       <h3>婚姻状态</h3>
       <p>{props.marital_status}</p>
    </div>
    <div className="clearfix"></div>
</div>    
<div className="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
   <div className="content">
     <div className="company">
       <h3 className="clr1">Previous Employment</h3>
       {props.experience !== '' &&
         props.experience.map((item, index) => {
         return (
             <div className="company_details">
               <h4> {item[3]} <span> {item[0]} </span></h4>
               <h6> {item[2]} <span> {item[4]} </span></h6>
               <p className="cmpny1">Nulla volutpat at est sed ultricies. In ac sem consequat, posuere nulla varius, molestie lorem. Duis quis nibh leo.
               Curabitur a quam eu mi convallis auctor nec id mauris. Nullam mattis turpis eu turpis tincidunt, et pellentesque leo imperdiet.
               Vivamus malesuada, sem laoreet dictum pulvinar, orci lectus rhoncus sapien, ut consectetur augue nibh in neque. In tincidunt sed enim et tincidunt.</p>
             </div>
          );   
       })}
     </div>
     <div className="skills">
       <h3 className="clr2">专业领域</h3>
       <div className="skill_list">
         <div className="skill1">
           <ul>
            {props.classify !== '' &&
              props.classify.map((item, index) => {
              return (<li> {item} </li>);   
            })}
           </ul>
         </div>
         <div className="clearfix"></div>
       </div>
     </div>
         <div className="copyrights">Collect from <a href="http://www.cssmoban.com/" >免费网站模板</a></div>
     <div className="education">
       <h3 className="clr3">Education</h3>
       {props.education_history !== '' &&
         props.education_history.map((item, index) => {
         return (
             <div className="education_details">
               <h4> {item[3]} <span> {item[0]} </span></h4>
               <h6> {item[1]} <span> {item[2]} </span></h6>
             </div>
          );   
       })}
     </div>
     <div className="copywrite">
       <p>Copyright &copy; 2015.Company name All rights reserved.More Templates <a href="http://www.cssmoban.com/" target="_blank" title="模板之家">模板之家</a> - Collect from <a href="http://www.cssmoban.com/" title="网页模板" target="_blank">网页模板</a></p>
     </div>
   </div>
</div>
</div>
    );
  }
}

Resume.propTypes = {
  style: PropTypes.object,
  dataSource: PropTypes.shape({
    name: PropTypes.string,
    gender: PropTypes.string,
    age: PropTypes.string,
    marital_status: PropTypes.string,
    education: PropTypes.string,
    school: PropTypes.string,
    position: PropTypes.string,
    company: PropTypes.string,
    classify: PropTypes.arrayOf(PropTypes.string),
    experience: PropTypes.shape({
      position: PropTypes.arrayOf(
        PropTypes.shape({
          at_company: PropTypes.number,
          date_from: PropTypes.string,
          date_to: PropTypes.string,
          duration: PropTypes.string,
          name: PropTypes.string,
        })
      ),
      company: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number,
          date_from: PropTypes.string,
          date_to: PropTypes.string,
          duration: PropTypes.string,
          name: PropTypes.string,
        })
      ),
    }),
    education_history: PropTypes.arrayOf(
      PropTypes.shape({
        date_from: PropTypes.string,
        date_to: PropTypes.string,
        education: PropTypes.string,
        major: PropTypes.string,
        school: PropTypes.string,
      })
    )
  })
};

export default Resume;