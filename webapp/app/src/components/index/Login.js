import React, { Component } from 'react';

import { Card, Form, Input, Button, Row, Col } from 'antd';

class Login extends Component {
  constructor(props) {
    super(props);
    this.handleOnSignIn = this.handleOnSignIn.bind(this);
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
        { min: 6, max: 12, message: 'Invalid Password. (At least 6-12 characters)' },
      ],
    });

    return (
      <div>
        <Card title="Sign in" bordered={true} style={{ width: 360, margin: '0 auto', marginTop: 90 }}>
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

export default Login = Form.create({})(Login);