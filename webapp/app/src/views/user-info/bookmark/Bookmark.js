'use strict';
import React, { Component, PropTypes } from 'react';

import TablePlus from 'components/table-plus';

class Bookmark extends Component {
  render() {
    const props = this.props;

    return (
      <TablePlus
        {...props}
        dataSource={props.bookmarkList}
      />
    );
  }
}

Bookmark.defaultProps = {
  bookmarkList: [],
};

Bookmark.propTypes = {
  bookmarkList: PropTypes.array,
};

export default Bookmark;
