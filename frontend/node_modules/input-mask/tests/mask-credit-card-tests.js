/* global describe, it */

var assert = require('assert'),
    inputMask = require('../input-mask');

describe('credit card', function () {

  var cc = inputMask('{9}{9}{9}{9} {9}{9}{9}{9} {9}{9}{9}{9} {9}{9}{9}{9}');

  it('should return empty credit card (empty input)', function () {

    assert.strictEqual( cc('').value, '' );

  });

  it('should return formatted credit card (flat input)', function () {

    assert.strictEqual( cc('5555555555554444').value, '5555 5555 5555 4444' );
    assert( cc('5555555555554444').filled );

  });

  it('should return formatted credit card (formatted input)', function () {

    assert.strictEqual( cc('5555 5555 5555 4444').value, '5555 5555 5555 4444' );
    assert( cc('5555 5555 5555 4444').filled );

  });

  it('should return partial formatted credit card (partial input)', function () {

    assert.strictEqual( cc('5555').value, '5555 ' );
    assert.strictEqual( cc('55555555').value, '5555 5555 ' );
    assert.strictEqual( cc('5555 5555').value, '5555 5555 ' );
    assert.strictEqual( cc('555555555555').value, '5555 5555 5555 ' );
    assert.strictEqual( cc('5555 5555 5555').value, '5555 5555 5555 ' );

  });

  it('should remove last separator (input + previousInput)', function () {

    assert.strictEqual( cc('5555', '5555 ').value, '555' );
    assert.strictEqual( cc('5555 5555', '5555 5555 ').value, '5555 555' );
    assert.strictEqual( cc('1234 5678', '1234 5678 ').value, '1234 567' );

  });

});
