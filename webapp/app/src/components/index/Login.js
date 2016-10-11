import React, { Component, PropTypes } from 'react';

import { Card, Form, Input, Button, Row, Col, Select } from 'antd';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      projectList: [],
    };
    this.handleOnSignIn = this.handleOnSignIn.bind(this);
    this.loadProjectList = this.loadProjectList.bind(this);
  }

  handleOnSignIn() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onSignIn(values);
      }
    });
  }

  loadProjectList() {
    fetch(`/api/projectnames`, {
      method: 'GET',
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          projectList: json.data,
        });
      }
    })
  }

  componentDidMount() {
    this.loadProjectList();
  }

  render() {
    const { getFieldProps } = this.props.form;

    const accountProps = getFieldProps('account', {
      rules: [
        { required: true, message: 'Account is required.' },
      ],
    });

    const pwdProps = getFieldProps('password', {
      rules: [
        { required: true, message: 'Password is required.' },
        { min: 6, max: 18, message: 'Invalid Password. (At least 6-12 characters)' },
      ],
    });

    const pjProps = getFieldProps('project', {
      rules: [
        { required: true, message: 'Project is required.' }
      ],
    });

    return (
      <div>
        <Card title="Sign in" bordered={true} style={{ width: 360, margin: '0 auto', marginTop: 80 }}>
          <Form horizontal>
            <Form.Item
              label="Account"
              id="account"
            >
              <Input {...accountProps} placeholder="Please input account." />
            </Form.Item>
            <Form.Item
              label="Password"
              id="password"
            >
              <Input {...pwdProps} type="password" placeholder="Please input password." />
            </Form.Item>
            <Form.Item
              label="Project"
              id="project"
            >
              <Select {...pjProps}>
                {this.state.projectList.map((item, index) => {
                  return <Select.Option key={index} value={item}>{item}</Select.Option>
                })}
              </Select>
            </Form.Item>
            <Row>
              <Col span="15" offset="9">
                <Form.Item>
                  <Button type="primary" style={{ margin: '0 auto' }} onClick={this.handleOnSignIn}>Sign in</Button>
                </Form.Item>
              </Col>
            </Row>
            
          </Form>
        </Card>
      </div>
    );
  }
}

Login.propTypes = {
  onSignIn: PropTypes.func.isRequired,
};

export default Login = Form.create({})(Login);