define(function() {

    function ColorGrad() {
        this.startColor = '#00FF00';
        this.endColor = '#FF0000';
        this.step = 100;
    }

    function hexToRgb(hex) {
        var rgb = [];
        for (var i = 1; i < 7; i += 2) {
            rgb.push(parseInt("0x" + hex.slice(i, i + 2)));
        }
        return rgb;
    }

    function rgbToHex(r, g, b) {
        var hex = ((r << 16) | (g << 8) | b).toString(16);
        return "#" + new Array(Math.abs(hex.length - 7)).join("0") + hex;
    }

    ColorGrad.prototype.gradient = function(option) {
        var sColor = hexToRgb(this.startColor),
            eColor = hexToRgb(this.endColor);

        var rC = (eColor[0] - sColor[0]) / this.step;
        var gC = (eColor[1] - sColor[1]) / this.step;
        var bC = (eColor[2] - sColor[2]) / this.step;

        var gradientColorArray = [];
        for (var i = 0; i < this.step; i++) {
            gradientColorArray.push(rgbToHex(parseInt(rC * i + sColor[0]), gC * i + sColor[1], bC * i + sColor[2]));
        }

        //Reverse the array
        gradientColorArray = gradientColorArray.reverse();

        var index = option - 1;

        return gradientColorArray[index];
    };

    return function() {
        return new ColorGrad();
    };
});
