import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import HeaderComponent from './components/HeaderComponent';
import TableComponent from './components/TableComponent';

const tableOptions = {
  headKey: ['ID', 'Name']
};

export default class UserManageView extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      data: []
    };
  }

  componentDidMount() {
    fetch('http://0.0.0.0:4888/api/accountlist')
    .then(response => response.json())
    .then(json => this.setState({data: json.data}));
  }

  render() {
    return (
      <div>
        <HeaderComponent {...this.props} />
        <Card
          style={{ width: 1080, margin: '0 auto', marginTop: 20 }}
        >
          <CardHeader
            title='User Management'
            titleStyle={{ fontSize: 20, color: '#555'}}
            style={{ backgroundColor: '#eee' }}
          />
          <CardText>
              <TableComponent options={ tableOptions } data={ this.state.data } />
          </CardText>
        </Card>
      </div>

    );
  }
}
