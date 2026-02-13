/* global define, navigator */

(function (root) {

var is_android = typeof navigator !== 'undefined' && navigator.userAgent.indexOf('Android') !== -1;

function bindInput (input, options) {
  options = options || {};

  var previous_value = input.value,
      mask_filled = null,
      noop = function () {};

  var _inputMask = options.mask instanceof Function ? options.mask : null;
  var applyMask = _inputMask ? function () {
    var result = _inputMask(input.value, previous_value);
    input.value = result.value;
    mask_filled = result.filled;
  } : noop;

  function getErrorKey () {
    if( !input.value && input.getAttribute('required') !== null ) return 'required';
    if( options.customError ) return options.customError(input.value, mask_filled);
    return '';
  }

  var onChange = options.onChange || noop;

  function onInput (_e) {
    applyMask();
    onChange.apply(input, [input.value, previous_value, mask_filled, getErrorKey() ]);
    previous_value = input.value;
  }

  input.addEventListener( is_android ? 'keyup' : 'input' , onInput, options.useCapture );

  input.addEventListener('blur' , function (e) {
    if(input.value !== previous_value) onInput(e);
  }, options.useCapture );

  return input;
}

if( typeof exports === 'object' && typeof module !== 'undefined' ) module.exports = bindInput;
else if( typeof define === 'function' && define.amd ) define([], function () { return bindInput; });
else root.bindInput = bindInput;

})(this);
