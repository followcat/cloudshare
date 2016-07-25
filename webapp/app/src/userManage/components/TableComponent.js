import React from 'react';

import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn } from 'material-ui/Table';
import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';

import CreateUserComponent from './CreateUserComponent';

const style = {
  color: '#fff'
};

export default class TableComponent extends React.Component {
  constructor(props) {
    super(props);

  }

  render() {
    return (
      <div>
        <Toolbar
          style={{ backgroundColor: '#fff' }}
        >
        <ToolbarGroup>
          <CreateUserComponent 
            { ...this.props }
          />
        </ToolbarGroup>
        </Toolbar>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHeaderColumn>ID</TableHeaderColumn>
              <TableHeaderColumn>Name</TableHeaderColumn>
              <TableHeaderColumn>Operate</TableHeaderColumn>
            </TableRow>
          </TableHeader>
          <TableBody>
            {
              this.props.data.map(function(user, index) {
                return (
                  <TableRow key={index}>
                    <TableRowColumn>{ index+1 }</TableRowColumn>
                    <TableRowColumn>{ user }</TableRowColumn>
                    <TableRowColumn>
                      <RaisedButton 
                        label="Delete" 
                        backgroundColor="#337ab7"
                        labelStyle={{ color: '#fff' }}
                      />
                    </TableRowColumn>
                  </TableRow>
                );
              })
            }
          </TableBody>
        </Table>
      </div>
    );
  }
}
