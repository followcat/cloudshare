'use strict';
/**
 * Deal with cv format, makes cv display beautiful.
 */

function Process(element) {
  this.__cvElement__ = element;
}

/**
 * Delete the hr tag element 
 * @return {None}
 */
Process.prototype.deleteHrTag = function() {
  let hrs = this.__cvElement__.getElementsByTagName('hr');

  for (let i = 0, len = hrs.length; i < len; i++) {
    hrs[i].remove();
  }
};

/**
 * Delete the h2 tag element if the id content value has 'section' string
 * @return {None}
 */
Process.prototype.deleteSectionTag = function() {
  let reg = /section-\d+|section/,
      h2s = this.__cvElement__.getElementsByTagName("h2");

  for (let i = 0, len = h2s.length; i < len; i++) {
    let _id = h2s[i].getAttribute('id');
    if (reg.test(_id)) {
      h2s[i].remove();
    }
  }
};

function getChildrenLink(obj) {
  let childrens = obj.children;
  for (let i = 0, len = childrens.length; i < len; i++) {
    if (childrens[i].nodeName === 'A') {
      return childrens[i];
    }
  }
  return null;
}

/**
 * Delete the link tag element if it on paragraph
 * @return {None}
 */
Process.prototype.deleteLinkOnParagraph = function() {
  let reg = /[\u4e00-\u9fa5]+/,
      ps = this.__cvElement__.getElementsByTagName('p');
  
  for (let i = 0, len = ps.length; i < len; i++) {
    let aObj = getChildrenLink(ps[i]),
        text = aObj ? aObj.textContent : null;
    if (text && reg.test(text)) {
      aObj.remove();
    }
  }
};

function addBrOnText(obj) {
  let text = obj.textContent,
      chinesePattern = /[\u4e00-\u9fa5]{15,}/,
      linePattern = /-{3,}/g,
      br1 = /；|;/g,
      br2 = /。/g;

  if (linePattern.test(text)) {
    text = text.replace(linePattern, '');
    obj.textContent = text;
  }

  if (chinesePattern.test(text)) {
    text = text.replace(br1, '；<br />');
    text = text.replace(br2, '。<br />');
    obj.innerHTML = text;
  }
}

/**
 * Delete the line
 * @return {None}
 */
Process.prototype.deleteLine = function() {
  let pattern = /-{3,}/g,
      ps = this.__cvElement__.getElementsByTagName("p"),
      ths = this.__cvElement__.getElementsByTagName("th"),
      tds = this.__cvElement__.getElementsByTagName("td");

  for (let i = 0, len = ths.length; i < len; i++) {
    let text = (ths[i] && ths[i].textContent) ? ths[i].textContent : '';
    if (pattern.test(text)) {
      ths[i].parentElement.remove();
    }
  }

  for (let i = 0, len = ps.length; i < len; i++) {
    let reg = /^(&nbsp;)(&nbsp;)*(&nbsp;)$/,
        _this = ps[i];

    if (reg.test(_this.innerHTML)) {
      _this.remove();
    }

    addBrOnText(_this);
  }

  for (let i = 0, len = tds.length; i < len; i++) {
    addBrOnText(tds[i]);
  }
};

/**
 * Concat two td cell if the second element html content is null
 * @return {None}
 */
Process.prototype.concatTd = function() {
  let tds = this.__cvElement__.getElementsByTagName('td');

  for (let i = 0, len = tds.length; i < len; i++) {
    let nextElement = tds[i].nextElementSibling;

    if (nextElement.innerHTML === '') {
      nextElement.remove();
      tds[i].setAttribute('colspan', '2');
    }
  }
};

/**
 * Get the hash value
 * @param  {string}
 * @return {string}
 */
function hashcode(str) {
  var hash = 0, i, chr, len;
  if (str.length === 0) return hash;
  for (i = 0, len = str.length; i < len; i++) {
    chr   = str.charCodeAt(i);
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
}

/**
 * If the sub node of current node has table tag element, return true 
 * @param  {object}
 * @return {Boolean}
 */
function isTableTagExisted(obj) {
  var childNodeList = obj.children;
  for (var i = 0, len = childNodeList.length; i < len; i++) {
    if (childNodeList[i].nodeName === "TABLE") {
      return true;
    }
  }
  return false;
}

/**
 * Genarate html
 * @param  {object}
 * @return {[object]}
 */
function htmlObjectGenarator(obj) {
  var htmlObj = {
          "hash": "",
          "html": "",
        };
  htmlObj.hash = hashcode(obj.outerHTML.toString().trim());
  htmlObj.html = obj.outerHTML.toString().trim();
  return htmlObj;
}

/**
 * Refactor table html content
 * @param  {object}
 * @return {array}
 */
function refactorTable(elementObj) {
  var tableList = elementObj.getElementsByTagName("table"),
      htmlArray = [];
  if (tableList.length > 0) {
    for (var i = 0, tableLen = tableList.length; i < tableLen; i++) {
      var tdListOnTable = tableList[i].getElementsByTagName("td"),
          isExisted = false;
      for (var j = 0, tdLen = tdListOnTable.length; j < tdLen; j++) {
        if (isTableTagExisted(tdListOnTable[j])) {
          isExisted = true;
          break;
        } else {
          isExisted = false;
        }
      }

      if (!isExisted) {
        htmlArray.push(htmlObjectGenarator(tableList[i]));
      }
    }
  } else {
    htmlArray.push(htmlObjectGenarator(elementObj));
  }

  return htmlArray;
}

/**
 * Refactor cv wrapper html content
 * @return {None}
 */
Process.prototype.refactorHTML = function() {
  let childrens = this.__cvElement__.getElementsByTagName('table'),
      htmlArray = [],
      htmlString = '';

  for (let i = 0, len = childrens.length; i < len; i++) {
    htmlArray = htmlArray.concat(refactorTable(childrens[i]));
  }

  for (let i = 0, len = htmlArray.length; i < len; i++) {
    htmlString += htmlArray[i].html;
  }

  this.__cvElement__.innerHTML = htmlString;

  if (this.callback && typeof this.callback === 'function') {
    this.callback();
  }
};

/**
 * Delete table width and style attribute
 * @return {None}
 */
Process.prototype.deleteTableAttribute = function() {
  let tables = this.__cvElement__.getElementsByTagName("table");
  if (tables.length > 0) {
    for (var i = 0, len = tables.length; i < len; i++) {
      tables[i].removeAttribute("width");
      tables[i].removeAttribute("style");
    }
  }
};

const CVProcess = {
  exec: function(element) {
    let processer = new Process(element);
    processer.refactorHTML();
    processer.deleteTableAttribute();
    processer.deleteHrTag();
    processer.deleteSectionTag();
    processer.deleteLinkOnParagraph();
    processer.deleteLine();
    processer = null;
  }
}

module.exports = CVProcess;
