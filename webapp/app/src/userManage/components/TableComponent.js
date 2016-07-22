import React from 'react';

import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';
import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import RaisedButton from 'material-ui/RaisedButton';

export default class TableComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  _renderTableRow() {
    this.props.data.map(function(user, index) {
      return (
        <TableRow>
          <TableRowColumn>{index+1}</TableRowColumn>
          <TableRowColumn>{user}</TableRowColumn>
          <TableRowColumn><RaisedButton label="Delete" primary={true} /></TableRowColumn>
        </TableRow>
      )
    });
  }

  render() {
    return (
      <div>
        <Toolbar
          style={{ backgroundColor: '#fff' }}
        >
          <ToolbarGroup>
            <RaisedButton 
              label="Crate New User" 
              backgroundColor="#337ab7"
              labelColor="#fff"
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
                        labelColor="#fff"
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
