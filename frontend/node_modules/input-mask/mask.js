/* global define */

(function (root) {

var matchValues = /{([a-z]+\:)?[\w\-]+}/g,
    matchParts = /{(([a-z]+)\:)?([\w\-]+)}/;

var transformers = {
  up: function (value) { return value.toUpperCase(); },
  lo: function (value) { return value.toLowerCase(); }
};

function inputMask (pattern) {
  var matchDigit = /\d/,
      markSeparators = pattern.split(matchValues).filter(function (v, i) { return !(i%2); }),
      patterns = pattern.match(matchValues).map(function (brackets) {
        if( brackets === '{9}' ) return matchDigit;
        var matches = brackets.match(matchParts);
        var pat = new RegExp('[' + matches[3] + ']');
        if( matches[2] ) {
          return {
            transform: transformers[matches[2]],
            test: pat.test.bind(pat)
          };
        }

        return pat;
      });

  function mask (value, previousValue) {
    var separators = markSeparators.slice(),
        result = '',
        letters = value.split(''),
        i, n, letter,
        p = 0;

    for( i = 0, n = letters.length; i < n ; i++ ) {
      if( !patterns[p] ) return { value: result, filled: true };
      letter = patterns[p].transform ? patterns[p].transform(letters[i]) : letters[i];

      if( patterns[p].test(letter) ) {
        result += separators[p] + letter;
        p++;
      } else if( letter === separators[p][0] ) {
        result += separators[p][0];
        separators[p] = separators[p].substr(1);
      } else {
        return { value: result, filled: false };
      }
    }

    if( previousValue && value.length < previousValue.length ) {
      return {
        value: previousValue.substr(-1) === separators[p][0] ? result.substr(0, result.length - 1) : result,
        filled: p === patterns.length
      };
    }

    return {
      value: result + separators[p],
      filled: p === patterns.length
    };
  }

  return mask;
}


if( typeof exports === 'object' && typeof module !== 'undefined' ) module.exports = inputMask;
else if( typeof define === 'function' && define.amd ) define([], function () { return inputMask; });
else root.mask = inputMask;

})(this);
