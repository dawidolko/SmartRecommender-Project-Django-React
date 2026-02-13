/* global describe, it */

var assert = require('assert'),
    inputMask = require('../input-mask');

describe('date', function () {

  var date = inputMask('{9}{9}/{9}{9}/{9}{9}{9}{9}');

  it('should return empty date (empty input)', function () {

    assert.strictEqual( date('').value, '' );

  });

  it('should return formatted date (flat input)', function () {

    assert.strictEqual( date('11121979').value, '11/12/1979' );
    assert( date('11121979').filled );

  });

  it('should return formatted date (formatted input)', function () {

    assert.strictEqual( date('11/12/1979').value, '11/12/1979' );
    assert( date('11/12/1979').filled );

  });

  it('should return formatted date (partial input)', function () {

    assert.strictEqual( date('11').value, '11/' );
    assert.strictEqual( date('11/').value, '11/' );
    assert.strictEqual( date('1112').value, '11/12/' );
    assert.strictEqual( date('11/12').value, '11/12/' );

  });

  it('should remove last separator (input + previousInput)', function () {

    assert.strictEqual( date('11', '11/').value, '1' );
    assert.strictEqual( date('11/12', '11/12/').value, '11/1' );

  });

});
