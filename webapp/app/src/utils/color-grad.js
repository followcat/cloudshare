'use strict';

const hexToRgb = (hex) => {
  let rgb = [];
  for (let i = 1; i < 7; i += 2) {
    rgb.push(parseInt('0x' + hex.slice(i, i + 2)));
  }
  return rgb;
};

const rgbToHex = (r, g, b) => {
  let hex = ((r << 16) | (g << 8) | b).toString(16);
  return '#' + new Array(Math.abs(hex.length - 7)).join('0') + hex;
};

class ColorGrad {
  constructor() {
    this.startColor = '#00FF00';
    this.endColor = '#FF0000';
    this.step = 100;
  }

  gradient() {
    const sColor = hexToRgb(this.startColor),
          eColor = hexToRgb(this.endColor);

    const rC = (eColor[0] - sColor[0]) / this.step,
          gC = (eColor[1] - sColor[1]) / this.step,
          bC = (eColor[2] - sColor[2]) / this.step;

    let gradientColorArray = [];
    for (let i = 0; i < this.step; i++) {
      gradientColorArray.push(rgbToHex(parseInt(rC * i + sColor[0]), gC * i + sColor[1], bC * i + sColor[2]));
    }

    gradientColorArray = gradientColorArray.reverse();
    return gradientColorArray;
  }
}

module.exports = ColorGrad;
