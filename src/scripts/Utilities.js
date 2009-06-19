// These are some handy utilities that are useful for writing good
// JavaScript code.  They are taken mostly from the book "JavaScript:
// the Good Parts" by Douglas Crockford.


// This create() method for the Object class makes it simpler to
// "subclass" or copy an object.  This is done by basing the new
// object's prototype on the argument to the create function.
if (typeof Object.create !== 'function') {
    Object.create = function(o) {
	var F = function () {};
	F.prototype = o;
	return new F();
    };
};

// A handy function method() for adding methods to arbitrary objects.
Function.prototype.method = function(name, func) {
    this.prototype[name] = func;
    return this;
};

// Use the inherits() method to create an inheritence relationship
// between two existing objects.  This is a "pseudo-classical" form of
// inheritance very similar to other OOP languages, but it's probably
// not the best form of inheritence in JavaScript
Function.method('inherits', function(Parent) {
	this.prototype = new Parent();
	return this;
    });


// Use the superior() method to access a superclass method when using
// the "functional" form f inherintance.
Object.method('superior', function(name) {
	var that = this,
	    method = that[name];
	return function() {
	    return method.apply(that, argument);
	};
    });
    
// List all of the properties of an object.
Object.method('list_properties', function(own_properties_only) {
	for (property in this) {
	    if (this.hasOwnProperty(property)) {
		print(property);
	    }
	}});

// List all properties including those up the
// prototype chain.
Object.method('list_all_properties', function(own_properties_only) {
	for (property in this) {
	    print(property);
	};
    });
