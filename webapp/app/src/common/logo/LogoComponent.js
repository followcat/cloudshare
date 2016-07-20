import React from 'react';
import ReactDOM from 'react-dom';


export default class LogoComponent extends React.Component {

  constructor(props) {

    super(props);

    this.state = {
      styles: {
        display: 'inline-block',
        position: 'absolute',
        top: '50%',
        marginTop: 0
      }
    };
  }

  componentDidMount() {
    let height = -ReactDOM.findDOMNode(this.refs.logo).offsetHeight / 2;
    this.setState({
      styles: {
        display: 'inline-block',
        position: 'absolute',
        top: '50%',
        marginTop: height + 'px'
      }
    });
  }

  render() {
    let aHref = this.props.href !== '' ? this.props.href : '#';

    return (
      <a href={ aHref } style={ this.state.styles } ref='logo'>
        <img src={ this.props.imgURL } alt='logo' />
      </a>
    );
  }
}
