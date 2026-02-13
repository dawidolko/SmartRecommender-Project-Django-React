/* global define, navigator */

(function (root) {

var isAndroid = typeof navigator !== 'undefined' && navigator.userAgent.indexOf('Android') !== -1;

var matchValues = /{([a-z]+:)?[\w-]+}/g,
    matchParts = /{(([a-z]+):)?([\w-]+)}/;

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

  var getValidityError = function (result, options, required) {
    var validityError = '';

    if( !result.value ) return required ? 'required' : '';

    if( options.customError ) {
      validityError = options.customError(result.value, result.filled);
      if( validityError ) return validityError;
    }

    if( options.validators ) for( var key in options.validators ) {
      if( !options.validators[key](result.value, result.filled) ) return key;
    }

    return result.filled ? '' : 'uncomplete';
  };

  mask.getValidityError = function (result, options, required) {
    return getValidityError( typeof result === 'string' ? mask(result) : result, options, required );
  };

  mask.bindTo = function (input, options) {
    options = options || {};

    var previousValue = input.value,
        eventNames = [isAndroid ? 'keyup' : 'input', 'blur'],
        listeners = {};

    var on = function (eventName, handler) {
      if( typeof handler !== 'function' ) throw new Error('handler should be a function');
      listeners[eventName] = listeners[eventName] || [];
      listeners[eventName].push(handler);
    };

    var emit = function (eventName, args) {
      (listeners[eventName] || []).forEach(function (listener) {
        listener.apply(input, args || []);
      });
    };

    var validityEmit = function (result, validationMessage, changed) {
      input.setCustomValidity(validationMessage);
      if( changed ) emit('change', [result.value, result.filled]);
    };

    function getErrorMessage () {
      for( var i = 0, n = arguments.length; i < n ; i++ ) {
        if( options.errorMessages[arguments[i]] ) return options.errorMessages[arguments[i]];
      }
      return '';
    }

    var updateInput = function (result) {
      var validityError, changed = result.value !== previousValue;

      previousValue = result.value;
      input.value = result.value;

      if( !options.errorMessages ) return emit('change', [result.value, result.filled]);

      validityError = getValidityError(result, options, input.getAttribute('required') !== null );

      validityEmit(
        result,
        validityError === 'uncomplete' ?
          getErrorMessage('uncomplete', 'pattern') :
          getErrorMessage(validityError),
        changed
      );
    };

    var handler = function (_e) {
      var result = options.preMask ? options.preMask(input.value, previousValue) : null;

      if( typeof result === 'string' ) return updateInput({ value: result, filled: mask(result).filled });
      else if( result ) return updateInput(result);

      result = mask(input.value, previousValue);

      if( !options.postMask ) return updateInput( result );

      result = { value: options.postMask(result.value, previousValue) };
      result.filled = mask(result.value).filled;

      return updateInput(result);
    };

    eventNames.forEach(function (eventName) {
      input.addEventListener(eventName, handler, options.useCapture );
    });

    return {
      applyMask: handler,
      on: on,
      emit: emit,
      input: input,
      setValue: function (value) {
        input.value = value;
        handler();
      },
      unbind: function ( _eventNames ) {
        ( _eventNames || eventNames ).forEach(function (eventName) {
          input.removeEventListener(eventName, handler, options.useCapture );
        });
      }
    };

  };

  return mask;
}

if( typeof exports === 'object' && typeof module !== 'undefined' ) module.exports = inputMask;
else if( typeof define === 'function' && define.amd ) define([], function () { return inputMask; });
else root.mask = inputMask;

})(this);
