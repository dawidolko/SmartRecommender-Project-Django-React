/* global describe, it */

var assert = require('assert'),
    inputMask = require('../input-mask');

describe('rfc', function () {

  var rfc = inputMask('{up:A-Z}{up:A-Z}{up:A-Z}{up:A-Z}{9}{9}{9}{9}{9}{9} {up:A-Z}{up:A-Z}{up:A-Z}');

  it('should return empty rfc (empty input)', function () {

    assert.strictEqual( rfc('').value, '' );

  });

  it('should return formatted rfc (flat input lowercase)', function () {

    assert.strictEqual( rfc('abcd123456xyz').value, 'ABCD123456 XYZ' );
    assert( rfc('abcd123456xyz').filled );

  });

  it('should return formatted rfc (flat input)', function () {

    assert.strictEqual( rfc('ABCD123456XYZ').value, 'ABCD123456 XYZ' );
    assert( rfc('ABCD123456XYZ').filled );

  });

  it('should return formatted rfc (formatted input lowercase)', function () {

    assert.strictEqual( rfc('abcd123456 xyz').value, 'ABCD123456 XYZ' );
    assert( rfc('abcd123456 xyz').filled );

  });

  it('should return formatted rfc (formatted input)', function () {

    assert.strictEqual( rfc('ABCD123456 XYZ').value, 'ABCD123456 XYZ' );
    assert( rfc('ABCD123456 XYZ').filled );

  });

  it('should return partial formatted rfc (partial input)', function () {

    assert.strictEqual( rfc('abcd123').value, 'ABCD123' );
    assert.strictEqual( rfc('ABCD123').value, 'ABCD123' );
    assert.strictEqual( rfc('abcd123456').value, 'ABCD123456 ' );
    assert.strictEqual( rfc('ABCD123456').value, 'ABCD123456 ' );

  });

  it('should remove last separator (input + previousInput)', function () {

    assert.strictEqual( rfc('abcd123456', 'abcd123456 ').value, 'ABCD12345' );
    assert.strictEqual( rfc('ABCD123456', 'ABCD123456 ').value, 'ABCD12345' );

  });

});
