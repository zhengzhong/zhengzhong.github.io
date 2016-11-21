---
layout: post
title: Notes: Eloquent JavaScript: Part 1: Language
categories: ['coding']
---

**Contents:**

- Values, Types, and Operators
- Program Structure
- Functions
- Data Structures: Objects and Arrays
- Higher-order Functions
- The Secret Life of Objects
- Project: Electronic Life
- Bugs and Error Handling
- Regular Expressions
- Modules
- Project: A Programming Language


## Values, Types, and Operators

Types as returned by `typeof`:

- `number`: integer or floating number.
- `string`: text.
- `boolean`: `true` or `false`.
- `object`
- `undefined`
- `function`

JavaScript does not distinguish integers and floating numbers. They are both of the `number` type.

There are 3 special numbers:

- `NaN` stands for "not a number". Any numerical operation that does not yield a precise,
  meaningful result will return `NaN`. For example: `0 / 0` or `Infinity - Infinity`.
- `Infinity` and `-Infinity`: represent the positive and negative infinities. Infinity-based
  computation is not reliable and can easily lead to `NaN`.

Note: `NaN` is the only value that is not equal to itself. To test if a value is `NaN`, use the
built-in function `isNaN()`.

```js
console.log(typeof NaN);        // number
console.log(typeof Infinity);   // number
console.log(typeof -Infinity);  // number
console.log(NaN == NaN);        // false
```

There are two special values, `null` and `undefined`, that are used to denote the absence of a
meaningful value. They are themselves values, but they carry no information.

Many operations that don't produce a meaningful value yield `undefined` simply because they have to
yield some value.

The difference in meaning between `undefined` and `null` is an accident of JavaScript's design.
Most of the time they can be treated as interchangeable.

```js
console.log(typeof undefined);    // undefined
console.log(typeof null);         // object
console.log(undefined == null);   // true
console.log(undefined === null);  // false
```

The `typeof` unary operator returns a string representing the right-hand-side operand.

### Automatic Type Conversion (Type Coercion)

When an operator is applied to the "wrong" type of value, JavaScript will quietly convert that
value to the type it wants, using a set of complicated rules. This is called *type coercion*.

When something that doesn't map to a number in an obvious way is converted to a number, the value
`NaN` is produced. Further arithmetic operations on `NaN` keep producing `NaN`.

```js
console.log(8 * null);    // 0
console.log(null * '8');  // 0
console.log('5' - 2);     // 3
console.log('5' - '2');   // 3
console.log('5' + 2);     // 52
console.log(5 + '2');     // 52
console.log('five' * 2);  // NaN
```

When comparing values of different types using `==`, in most cases, JavaScript tries to convert
one of the values to the other value's type. However, when `null` or `undefined` occurs on either
side of the operator, it produces `true` only if both sides are one of `null` or `undefined`.

```js
console.log(false == 0);         // true
console.log(false == '0');       // true
console.log('0' == false);       // true
console.log(0 == '0');           // true
console.log(null == 0);          // false
console.log(null == undefined);  // true
```

To disable type coercion when comparing values, use `===` and `!==`. These two three-character
comparison operators test precise equality of two values.

Conclusions:

- JavaScript's type coercion is not reliable and should be avoided.
- To test whether a value has a real value instead of `null` or `undefined`, simply compare it to
  `null` with the `==` or `!=` operator.
- It's best practice to use `===` and `!==` defensively, to prevent unexpected type coercion.

### Short-Circuiting of Logical Operators

The logical operators `&&` and `||` will convert the value on their left side to `boolean` type in
order to decide what to do, but depending on the operator and the result of that conversion, they
return either the original left-hand value or the right-hand value.

```js
console.log(null || 'default value');  // default value
console.log('X' || 'default value');   // X
console.log(0 || 'default value');     // default value
console.log('0' || 'default value');   // 0
```

This allows the `||` operator to be used as a way to fall back on a default value.

These operators use short-circuit evaluation: the expression to their right is evaluated only when
necessary. The conditional operator (`condition ? value_if_true : value_if_false` ) works in a
similar way: the first expression (`condition`) is always evaluated, but the second
(`value_if_true`) or third value (`value_if_false`), the one that is not picked, is not.


## Program Structure

*No particularities comparing to other languages.*


## Functions

### Defining a Function

A *function definition* is just a regular variable definition where the value given to the variable
happens to be a function.

```js
var square = function(x) {
  return x * x;
};

console.log(square(12));  // 144
```

### Parameters and Scopes

A function can return a value. If a function uses the `return` keyword without an expression after
it, or if it does not have a `return` statement, it will return `undefined`.

Variables created inside of a function, including its parameters, are local to the function. They
will be newly created every time the function is called, and these separate incarnations do not
interfere with each other.

This "localness" of variables applies only to the parameters and to variables declared with the
`var` keyword inside the function body. Variables declared outside of any function are called
global. It is possible to access such variables from inside a function, as long as they are not
collapsed by a local variable with the same name.

### Nested Scope

Functions can be created inside other functions, producing several degrees of locality. In short,
each local scope can also see all the local scopes that contain it. The set of variables visible
inside a function is determined by the place of that function in the program text. All variables
from blocks around a function's definition are visible, meaning both those in function bodies that
enclose it and those at the top level of the program. This approach to variable visibility is
called *lexical scoping*.

In JavaScript, functions are the only things that create a new scope. A block of code between
braces does **NOT** produce a new local environment.

```js
var a = 1;
for (var b = 2; b < 10; b++) {
  if (b < 10) {
    c = 3;
  } else {
    d = 4;
  }
}

console.log('a = ' + a);  // a = 1
console.log('b = ' + b);  // b = 10
console.log(typeof c !== 'undefined' ? 'c = ' + c : 'c is undefined');  // c = 3
console.log(typeof d !== 'undefined' ? 'd = ' + d : 'd is undefined');  // d is undefined
```

Note: The next version of JavaScript will introduce a `let` keyword, which works like `var` but
creates a variable that is local to the enclosing block, not the enclosing function.

### Declaration Notation

A *function declaration* looks like the following:

```js
function square(x) {
  return x * x;
};
```

Unlike function definitions, function declarations are not part of the regular top-to-bottom flow
of control. They are conceptually moved to the top of their scope and can be used by all the code
in that scope. This allows us to place a function declaration below the code that calls it.

Do **NOT** put a function definition inside a conditional (`if`) block or a loop. Different
JavaScript platforms in different browsers have traditionally done different things in that
situation, and the latest standard actually forbids it. Use function definitions only in the
outermost block of a function or program.

```js
function example() {
  function a() {}  // Okay
  if (something) {
    function b() {}  // Danger!
  }
}
```

### Optional Arguments

It is legal to pass arbitrary number of parameters to a function, no matter how that function is
defined/declared. If you pass too many, the extra ones are ignored. If you pass too few, the
missing parameters simply get assigned the value `undefined`.

This behavior can be used to have a function take optional arguments. Inside a function, to check
if a parameter is passed in, just compare it with `undefined`.

### Closure

The ability to treat functions as values, combined with the fact that local variables are
"re-created" every time a function is called, brings up an interesting question: What happens to
local variables when the function call that created them is no longer active?

This feature -- being able to reference a specific instance of local variables in an enclosing
function -- is called *closure*. A function that "closes over" some local variables is called a
closure.

A good mental model is to think of the `function` keyword as "freezing" the code in its body and
wrapping it into a package (the function value). So when you read `return function(...) {...}`,
think of it as returning a handle to a piece of computation, frozen for later use.

```js
function multiplier(factor) {
  // The parameter 'factor' is a local variable. The function that is returned
  // below captures and freezes the variable into a piece of computation.
  return function(number) {
    return number * factor;
  };
}

var twice = multiplier(2);
console.log(twice(5));  // 10
```

### More on Closure

More on JavaScript closure: http://stackoverflow.com/questions/111102/

What is a closure?

- A closure is one way of supporting first-class functions; it is an expression that can reference
  variables within its scope (when it was first declared), assigned to a variable, passed as an
  argument to a function, or returned as a function result. Or...
- A closure is a stack frame which is allocated when a function starts its execution, and not freed
  after the function returns (as if a 'stack frame' were allocated on the heap rather than on the
  stack).

In JavaScript, a function reference variable can be seen as having both a pointer to a function as
well as a hidden pointer to a closure. In JavaScript, if you use the `function` keyword inside
another function, you are creating a closure.

**Example 1**

```js
var gLogNumber, gIncreaseNumber, gSetNumber;

function setupGlobals() {
  var num = 1;
  gLogNumber = function() {
    console.log('Number is ' + num);
  };
  gIncreaseNumber = function() {
    num++;
  };
  gSetNumber = function(x) {
    num = x;
  };
}

setupGlobals();     // create closure: setupGlobals_closure_0 { num }
gLogNumber();       // print: 1 (setupGlobals_closure_0.num)
gIncreaseNumber();  // setupGlobals_closure_0.num becomes 2
gLogNumber();       // print: 2
gSetNumber(100);    // setupGlobals_closure_0.num becomes 100
gLogNumber();       // print: 100

setupGlobals();     // create a new closure: setupGlobals_closure_1 { num }
gLogNumber();       // print: 1 (setupGlobals_closure_1.num)
gIncreaseNumber();  // setupGlobals_closure_1.num becomes 2
gLogNumber();       // print: 2
gSetNumber(100);    // setupGlobals_closure_1.num becomes 100
gLogNumber();       // print: 100
```

Within `setupGlobals()`, a single closure is created holding a reference to the local variable
`num`. This closure is shared among the 3 global functions.

Calling `setupGlobals()` again will create a new closure.

**Example 2**

```js
function buildList(list) {
  var result = [];
  for (var i = 0; i < list.length; i++) {
    var item = 'item #' + i;
    result.push(function() {
      console.log(item + ': ' + list[i]);
    });
  }
  return result;
}

function testList() {
  var functions = buildList([1, 2, 3]);
  // Calling `buildList()` creates one single closure: { list, result, i, item } which is shared
  // by all the functions in the returned list. Values in the closure are:
  //
  // - list: [1, 2, 3];
  // - result: an array containing 3 functions;
  // - i: 3 (value after the `for` loop);
  // - item: 'item #2' (the last value as updated in the `for` loop);

  for (var i = 0; i < functions.length; i++) {
    functions[i]();
  }
  // This will print out 3 times: item #2: undefined
}

testList();
```

After `buildList([1, 2, 3])` is called, a new closure is created holding the following references:

- `list`: the parameter: `[1, 2, 3]`.
- `result`: a local array containing 3 functions.
- `i`: the local variable used in the `for` loop, with a value of `3` (`list.length`).
- `item`: the local variable inside the `for` loop, with a value of `item #2` (the last iteration
  of the `for` loop).

This closure is shared among the 3 functions in the returned array.

When these functions are called, they will each print `item #2: undefined`. The `undefined` comes
from `list[i]` where `i` is out of bound.

**Final Points**

- Whenever you use `function` inside another function, a closure is used. It is probably best to
  think that a closure is always created just on entry to a function, and the local variables are
  added to that closure. Note that one single closure is created, and can be shared among several
  nested functions.
- A closure in JavaScript is like keeping a copy of all the local variables, just as they were when
  a function exited.
- A function doesn't have to return in order to be called a closure. Simply accessing variables
  outside of the immediate lexical scope creates a closure.
- When you use `new Function(...)` (the `Function` constructor) inside a function, it does not
  create a closure. The new function cannot reference local variables of the outer function.


### Functions and Side Effects

A *pure function* is a specific kind of value-producing function that not only has no side effects
but also doesn't rely on side effects from other code. A pure function, when called with the same
arguments, always produces the same value (and doesn't do anything else).


## Data Structures: Objects and Arrays

### Properties and Methods

Almost all JavaScript values have properties. The exceptions are `null` and `undefined`.

The two most common ways to access properties in JavaScript are with dot notation and with square
brackets. Both `value.x` and `value['x']` access the property `x` on `value`. These 2 expressions
are equivalent. For example, to get the length of an array, one can use `array.length` or
`array['length']`.

Square brackets are typically used in the following scenarios:

- When a property name is not a valid variable name. For example, elements in an array are stored
  in properties whose names are numbers. So we use `array[0]` to access property `0` of `array` --
  the first element in the array. Another example is `value['property-name']`.
- When the property name is calculated dynamically.

Properties that contain functions are generally called methods of the value they belong to. For
example, an array object has methods like `push`, `pop`, etc.

### Objects

Values of the type `object` are arbitrary collections of properties. Properties are dynamic and can
be added or removed as we please. One way to create an object is by using a curly brace notation.

```js
var person = {
  name: 'ZHENG Zhong',
  skills: ['Java', 'C++', 'Python'],
  'phone number': '06 12 34 56 78',
  greeting: function() {
    console.log('Hello!');
  }
};
```

Reading a property that doesn't exist will produce `undefined`.

It is possible to assign a value to a property expression with the `=` operator. This will replace
the property's value if it already existed, or create a new property on the object if it didn't.

The `delete` operator removes a property from an object. Deleting a non-existent property has no
effect. Deleting an element of an array using its index will remove that number property from the
array, but will not change the array's length -- this creates a hole in the array.

The binary `in` operator, when applied to a string and an object, returns a `boolean` value that
indicates whether that object has that property. The difference between setting a property to
`undefined` and actually deleting it is that, in the first case, the object still has the property
whose value is `undefined`, whereas in the second case the property is no longer present and `in`
will return `false`.

Arrays, then, are just a kind of object specialized for storing sequences of things. So,
`typeof [1, 2]` will return `object`.

JavaScript provides a loop construct specifically for going over the properties of an object, using
the keyword `in`.

```js
for (var name in obj) {
  console.log(name + ' = ' + obj[name]);
}
```

An object can be used as a map (dictionary) to store key-value pairs.

### Mutability

Primitive types (`boolean`, `string` and `number`) are immutable. Values of primitive types can be
compared using `==` or `!=`.

Values of `object` type are mutable. JavaScript's `==` operator, when comparing objects, will
return `true` only if both objects are precisely the same value. Comparing different objects will
return `false`, even if they have identical contents. There is no "deep" comparison operation built
into JavaScript, which looks at object's contents.

### The Arguments Object

Whenever a function is called, a special variable named `arguments` is added to the environment in
which the function body runs. This variable refers to an object that holds all of the arguments
passed to the function.

### The Global Object

The global scope, the space in which global variables live, can also be approached as an object in
JavaScript. Each global variable is present as a property of this object. In browsers, the global
scope object is stored in the `window` variable.


## Higher-Order Functions

Functions that operate on other functions, either by taking them as arguments or by returning them,
are called *higher-order functions*.

### Applying a Function

JavaScript functions have an `apply` method, which calls a function with a given `this` value and
`arguments` provided as an array (or an array-like object):

    fun.apply(thisArg, [argsArray])

Where:

- `thisArg`: The value of `this` provided for the call to `fun`. Note that this may not be the
  actual value seen by the method: if the method is a function in non-strict mode code, `null` and
  `undefined` will be replaced with the global object, and primitive values will be boxed.
- `argsArray`: An array-like object, specifying the arguments with which `fun` should be called, or
  `null` or `undefined` if no arguments should be provided to the function.

The method returns the result of calling the function.

You can assign a different `this` object when calling an existing function. this refers to the
current object, the calling object. With `apply`, you can write a method once and then inherit it
in another object, without having to rewrite the method for the new object.

### JSON

JSON stands for JavaScript Object Notation. It is widely used as a data storage and communication
format on the Web. JSON is similar to JavaScript's way of writing arrays and objects, with a few
restrictions:

- All property names should be surrounded by double quotes.
- Only simple data expressions are allowed -- no function calls, variables, or anything that
  involves actual computation.
- Comments are not allowed.

JavaScript has functions, `JSON.stringify` and `JSON.parse`, that convert data from and to JSON.

### Higher-Order Functions in Array Object

Array object has several higher-order functions:

- `array.forEach(callback[, thisArg])`: Calls `callback(element, index, array)` with every element
  in this array.
- `array.filter(callback[, thisArg])`: Creates a new array with all elements that pass the test
  `callback(element, index, array)`.
- `array.map(callback[, thisArg])`: Creates a new array with the results of calling
  `callback(element, index, array)` on every element in this array.
- `array.reduce(callback[, initialValue])`: Applies `callback(previousValue, element, index, array)`
  against an accumulator and each element of the array (from left to right) to reduce it to a
  single value. **Note:** If `initialValue` isn't provided, it will execute `callback` starting at
  index 1, skipping the first index. If `initialValue` is provided, it will start at index 0.

Where possible arguments of the `callback()` function are:

- `element` is the current element being processed in the array;
- `index` is the index of the current element in the array;
- `array` is the array the higher-order function was called upon;
- `previousValue` (for reduce) is the value previously returned in the last invocation of the
  reduce callback, or `initialValue`, if supplied.

```js
var persons = [
  {name: 'Paul', sex: 'male', age: 40},
  {name: 'Marc', sex: 'male', age: 42},
  {name: 'Alice', sex: 'female', age: 22},
  {name: 'Jeff', sex: 'male', age: 44},
  {name: 'Claire', sex: 'female', age: 28}
];

// Print out all the names.
persons.forEach(function(person, index) {
  console.log('#' + index + ': ' + person.name);
});

// Filter out all males.
var males = persons.filter(function(person) {
  return person.sex === 'male';
});

// Converts males to an array of their ages.
var ages = males.map(function(male) {
  return male.age;
})

// Add up all the ages.
var totalAge = ages.reduce(function(previousValue, age) {
  return previousValue + age;
});

console.log('Average age of all males: ' + (totalAge / males.length));
```

### Binding

The `bind` method for a function creates a new function that will call the original function but
with some of the arguments already fixed.

    fun.bind(thisArg[, arg1[, arg2[, ...]]])

Parameters:

- `thisArg`: The value to be passed as the `this` parameter to the target function when the bound
  function is called.
- `arg1, arg2, ...`: Arguments to prepend to arguments provided to the bound function when invoking
  the target function.

It returns a copy of the given function with the specified `this` value and initial arguments.

The `bind` method creates a new bound function -- an exotic function object that wraps the original
function object. Calling a bound function generally results in the execution of its wrapped function.

### Function's `this` Variable

TODO: strict mode! global is null!

Each function, when called, has an implicit variable called `this`, which is the object upon which
the function is called.

- A free function is bound to the global object. When `this` is not bound otherwise, or when it is
  bound to `null` or `undefined`, it points to the global object.
- When a function is defined as an object method, it is bound to that object. Thus `this` points to
  the object on which the method is defined.
- The `apply`, `call` and `bind` methods of an function can bind `this` to another object.

```js
name = 'Global';  // Define a `name` property on the global object.

var bar = function() {
  console.log(this.name);
}

bar();             // Global
bar.apply(null);   // Global
bar.bind(null)();  // Global

obj = {name: 'Object'};
obj.bar = bar;
obj.bar();        // Object
bar.apply(obj);   // Object
bar.bind(obj)();  // Object
```

Because of this, you can get the global object by returning `this` from an unbound function:

```js
var getGlobalObject = function() {
  return (function() {
    return this;
  }).call(null);
}

var globalObject = getGlobalObject();
```

## The Secret Life of Objects

### Methods

Methods are simply properties that hold function values. Usually a method needs to do something
with the object it was called on. When a function is called as a method, the special variable
`this` in its body will point to the object that it was called on.

The `apply` and `bind` methods both take a first argument that can be used to simulate method calls.
This first argument is used to give a value to `this`.

There is a method similar to `apply`, called `call`. It also calls the function of which it is a
method, but takes its arguments normally, rather than as an array. Like `apply` and `bind`, `call`
can be passed a specific `this` value.

### Prototype

In addition to their set of properties, almost all objects also have a *prototype*. A prototype is
another object that is used as a fallback source of properties. When an object gets a request for a
property that it does not have, its prototype will be searched for the property, then the
prototype's prototype, and so on.

Every object has an ancestral prototype: `Object.prototype`. The `Object.getPrototypeOf` function
returns the prototype of an object.

**Note:** The object's prototype itself is not a property of that object.

```js
console.log(Object.getPrototypeOf({}) == Object.prototype);  // true
console.log(Object.getPrototypeOf(Object.prototype));        // null
```

The prototype relations of JavaScript objects form a tree-shaped structure, and at the root of this
structure sits `Object.prototype`. It provides a few methods that show up in all objects, such as
`toString` (which converts an object to a string representation).

Many objects don't directly have `Object.prototype` as their prototype, but instead have another
object, which provides its own default properties. Functions derive from `Function.prototype`, and
arrays derive from `Array.prototype`.

```js
console.log(Object.getPrototypeOf(isNaN) == Function.prototype);  // true
console.log(Object.getPrototypeOf([]) == Array.prototype);        // true
```

Such a prototype object will itself have a prototype, often `Object.prototype`, so that it still
indirectly provides methods like `toString`.

You can use `Object.create` to create an object with a specific prototype.

```js
var protoRabbit = {
  speak: function(something) {
    console.log('The ' + this.type + ' rabbit says: ' + something);
  }
};
var killerRabbit = Object.create(protoRabbit);
killerRabbit.type = 'killer';
killerRabbit.speak('SKREEEE!');

console.log(Object.getPrototypeOf(killerRabbit) === protoRabbit);      // true
console.log(Object.getPrototypeOf(protoRabbit) === Object.prototype);  // true
```

### Constructors

In JavaScript, calling a function with the `new` keyword in front of it causes it to be treated as
a constructor. The constructor will have its this variable bound to a fresh object, and unless it
explicitly returns another object value, this new object will be returned from the call.

An object created with new is said to be an instance of its constructor.

Constructors (in fact, all functions) automatically get a property named `prototype`, which by
default holds a plain, empty object that derives from `Object.prototype`. Every instance created
with this constructor will have this object as its prototype.

It is important to note the distinction between the way a prototype is associated with a
constructor (through its `prototype` property) and the way objects have a prototype (which can be
retrieved with `Object.getPrototypeOf`). The actual prototype of a constructor is
`Function.prototype` since constructors are functions. Its `prototype` property will be the
prototype of instances created through it but is not its own prototype.

```js
function Rabbit(type) {
  this.type = type;
}

// The constructor's prototype is Function.prototype.
// It is not the same as its 'prototype' property.
console.log(Object.getPrototypeOf(Rabbit) === Function.prototype);  // true
console.log(Object.getPrototypeOf(Rabbit) === Rabbit.prototype);    // false

// Rabbit.prototype (the 'prototype' property of the constructor)
// derives from Object.prototype.
console.log(Object.getPrototypeOf(Rabbit.prototype) === Object.prototype);  // true

// Override the `toString` method of Object.prototype.
Rabbit.prototype.toString = function() {
  return 'The ' + this.type + ' rabbit';
}

// Add a new method to Rabbit.prototype.
Rabbit.prototype.speak = function(something) {
  console.log(this + ' says: ' + something);
};

var rabbit = new Rabbit('killer');
rabbit.speak('Doom!');

// Test toString methods...
console.log(rabbit.toString());                       // The killer rabbit
console.log(Rabbit.prototype.toString.call(rabbit));  // The killer rabbit
console.log(Object.prototype.toString.call(rabbit));  // [object Object]

// Check prototypes...
console.log(Object.getPrototypeOf(Rabbit) === Function.prototype);  // true
console.log(Object.getPrototypeOf(Rabbit) === Rabbit.prototype);    // false
console.log(Object.getPrototypeOf(rabbit) === Rabbit.prototype);    // true
console.log(rabbit.prototype === undefined);                        // true
```

### Overriding Derived Properties

When you add a property to an object, whether it is present in the prototype or not, the property
is added to the object *itself*, which will henceforth have it as its own property. If there is a
property by the same name in the prototype, this property will no longer affect the object. The
prototype itself is not changed.

Overriding properties that exist in a prototype is often a useful thing to do. It can be used to
express exceptional properties in instances of a more generic class of objects, while letting the
nonexceptional objects simply take a standard value from their prototype.

### Prototype Interference

JavaScript distinguishes between enumerable and nonenumerable properties. All properties that we
create by simply assigning to them are enumerable. The standard properties in `Object.prototype`
are all nonenumerable.

 The `for/in` loop over an object will iterate through only enumerable properties, whilst the `in`
 operator will check both enumerable and nonenumerable properties.

```js
var obj = { name: 'Something' };
Object.prototype.category = 'Uncategorized';
Object.prototype.printCategory = function() {
  console.log('Category of ' + this + ' is ' + this.category);
};

// All the following checks will print 'true'.
console.log('name' in obj);
console.log('category' in obj);
console.log('printCategory' in obj);
console.log('toString' in obj);

// Following loop will print: 'name', 'category' and 'printCategory'.
for (var name in obj) {
  console.log(name);
}
```

It is possible to define nonenumerable properties by using the `Object.defineProperty` function,
which allows us to control the type of property we are creating. Defining a nonenumerable property
in this way will prevent it from showing up in the `for/in` loop. But nonenumerable properties can
still be checked with the `in` operator.

To check whether the object itself has a property without looking at its prototype, use the
`hasOwnProperty` method. Note that this method does not check if the property is enumerable or not.

```js
Object.defineProperty(Object.prototype, 'foo', {enumerable: false, value: 'bar'});

// The `foo` property will not show up in the following loop.
for (var name in obj) {
  console.log(name);
}

console.log(obj.foo);                    // bar
console.log('foo' in obj);               // true
console.log(obj.hasOwnProperty('foo'));  // false
```

To list all properties that belong to the object itself instead of its prototype, use the
`getOwnPropertyNames` method:

```js
obj.getOwnPropertyNames().forEach(function(name) {
  console.log(name);
});

// Equivalent to:
for (var name in obj) {
  if (obj.hasOwnProperty(name)) {
    console.log(name);
  }
}
```

To get all property names from an object, including those from the object itself and those from its
prototype(s), no matter if they are enumerable or not:

```js
function getAllPropertyNames(obj) {
  var allPropertyNames = [];
  for (var current = obj; current !== null; current = Object.getPrototypeOf(current)) {
    var ownPropertyNames = Object.getOwnPropertyNames(current);
    ownPropertyNames.forEach(function(name) {
      if (allPropertyNames.indexOf(name) === -1) {
        allPropertyNames.push(name);
      }
    });
  }
  return allPropertyNames;
}
```

### Prototype-less Objects

The `Object.create` function allows us to create an object with a specific prototype. If `null` is
passed as the prototype argument, a fresh object with no prototype is created.

```js
var obj1 = {name: 'object with a prototype'};
console.log('name' in obj1);      // true
console.log('toString' in obj1);  // true

var obj2 = Object.create(null);
obj2['name'] = 'object without prototype';
console.log('name' in obj2);      // true
console.log('toString' in obj2);  // false
```

This is useful to create a object which serves as a key-value map. For an object created this way,
we no longer need the `hasOwnProperty` kludge because all the properties the object has are its own
properties. We can safely use `for/in` loops and the `in` operator, no matter what people have been
doing to `Object.prototype`.

### Getters and Setters

JavaScript allows to define a dynamic property with `get` and/or `set` functions. A dynamic
property can be used from the outside just like a normal property.

```js
// Define getter / setter on an object directly...
var obj = {
  get dynamicProperty() {
    // Calculated value of the property.
    return calculatedValue;
  },
  set dynamicProperty(value) {
    // Process the value...
  }
};

// Define a constructor.
function Foo() {
  // ...
}

// Define getter / setter on Foo.prototype...
Object.defineProperty(Foo.prototype, 'dynamicProperty', {
  get: function() {
    // Calculated value of the property.
    return calculatedValue;
  },
  set: function(value) {
    // Process the value...
  }
});
```

Getting value from a dynamic property without `get` will return `undefined`. Setting value to a
dynamic property without `set` will be ignored.

### Inheritance and the `instanceof` Operator

Inheritance is about building a proper prototype chain.

The `instanceof` operator will see through inherited types (the prototype chain) to check whether
an object was derived from a specific constructor. It can be applied to standard constructors like
`Array`. Almost every object is an instance of `Object`.

```js
// Define a Base class.
function Base(value) {
  this.value = value;
}

Base.prototype.anotherValue = 'another-value';
Base.prototype.doSomething = function() {
  console.log('Doing something...');
};

// Define a Derived class which inherits from Base.
function Derived(value) {
  // Call base constructor with this.
  Base.call(this, value);
}

// Build the prototype chain so that Derived.prototype
// will have Base.prototype as its own prototype.
Derived.prototype = Object.create(Base.prototype);

// Override a property from the base prototype.
Derived.prototype.doSomething = function() {
  console.log('Doing something else...');
};

var obj = new Derived('my-value');
console.log(obj.value);         // my-value
console.log(obj.anotherValue);  // another-value
obj.doSomething();              // Doing something else...

console.log(obj instanceof Derived);  // true
console.log(obj instanceof Base);     // true
console.log(obj instanceof Object);   // true

console.log([] instanceof Array);     // true
console.log([] instanceof Object);    // true
```

### Final Notes about Objects

- Each object has a prototype, which holds a list of fallback properties.
- An object's prototype can itself has a prototype. This forms a prototype chain where the root is
  `Object.prototype`, whose prototype is `null`.
- The `Object.getPrototypeOf` function returns the prototype of an object.
- When accessing a property of an object, its own properties (those that are defined directly on
  the object) are firstly checked, then the properties in its prototype chain.
- A property is either enumerable or nonenumerable. Nonenumerable properties can be defined using
  the `Object.defineProperty` function. A `for/in` loop on an object will iterate through all its
  enumerable properties.
- The `hasOwnProperty` method checks whether a property is an object's own property (not in its
  prototype). The `in` operator checks whether a property belongs to an object. These two checks do
  not distinguish between enumerable and nonenumerable properties.
- The `getOwnPropertyNames` method returns an array of the object's own property names.
- The `Object.create` function can create an object from a given prototype. When the prototype
  argument is `null`, it creates an object without prototype (prototype-less).
- A constructor (a function called with `new`) creates an object. The constructor's `prototype`
  property is used as the prototype of the object it creates. Note that the constructor's own
  prototype is `Function.prototype`.
- Inheritance is about building a proper prototype chain.


## Bugs and Error Handling

### Strict Mode

Putting the string `'use strict'` at the top of a file or a function body will enable JavaScript's
*strict mode*. Two of the main differences are:

- In non-strict mode, declaring a variable without `var` will cause JavaScript to quietly create a
  global variable and use it. In strict mode, this is forbidden.
- In strict mode, the `this` binding holds `undefined` in functions that are not called as methods.
  When making such a call in non-strict mode, `this` refers to the global scope object.

Best practice is to always `'use strict'`.

### Exceptions

JavaScript provides a standard `Error` constructor that creates an error object with a `message`
property. In modern JavaScript environments, `Error` instances also gather information about the
call stack (stack trace) in the `stack` property.

To use selective catching, we can define a custom error constructor that derives from `Error`:

```js
function CustomError(message) {
  // Note: This will not work: Error.call(this, message);
  this.message = message;
  this.stack = (new Error()).stack;
}
CustomError.prototype = Object.create(Error.prototype);
CustomError.prototype.name = 'CustomError';

function CustomError(message) {
  this.message = message;
  this.stack = (new Error()).stack;
}
CustomError.prototype = Object.create(Error.prototype);
CustomError.prototype.name = 'CustomError';

// Selective catching...

function goWrong() {
  throw new CustomError('something is wrong!');
}

try {
  goWrong();
} catch (e) {
  if (e instanceof CustomError) {
    // Handle the custom error...
  } else {
    // Handle a generic error...
  }
} finally {
  // Final cleanup...
}
```

Note: `Error` is a function that returns a new Error object, and it does not manipulate `this` in
any way. That is why:

- `Error(message)` works as well without the `new` keyword.
- Using `Error.call(this, message)` in custom error constructor will not set any property (neither
  `message` nor `stack`) on the returned error object.

### Assertions

JavaScript does not have `assert`. To create an assert function:

```js
function AssertionFailed(message) {
  this.message = message;
}
AssertionFailed.prototype = Object.create(Error.prototype);

function assert(test, message) {
  if (!test) {
    throw new AssertionFailed(message);
  }
}
```


## Regular Expressions

### Creating a Regular Expression

A regular expression is a type of object. It can either be constructed with the `RegExp`
constructor or written as a literal value by enclosing the pattern in forward slashes (`/`).

```js
var regex1 = new RegExp('abc');
var regex2 = /abc/;
```

Adding an `i` character after the ending slash of a literal value makes the regular expression case
insensitive.

When using the `RegExp` constructor, the pattern is written as a normal string, so the usual rules
apply for backslashes.

When using the literal value notation, backslashes are treated differently:

- Any forward slash in the regular expression needs to be escaped by a backslash.
- Backslashes that aren't part of special character codes (like `\n`) will be preserved and does
  not need to be escaped.

Some characters, such as `?` and `+`, have special meanings in regular expressions. They must be
escaped by a backslash if they are meant to represent the character itself.

### Testing for Matches

The `test` method of a regular expression checks if the regular expression matches the given string
(the argument). This method returns `true` if there is a match anywhere in the string.

The characters `^` and `$` can be used to define string boundaries, where `^` matches the start of
a string, and `$` matches the end of a string.

The marker `\b` defines a word boundary. A word boundary can be the start or end of the string or
any point in the string that has a word character (as in `\w`) on one side and a nonword character
on the other.

There are a number of common character groups that have their own built-in shortcuts:

- `\d`: Any digit character, same as `[0-9]`.
- '\w': An alphanumeric character ("word character"), same as `[a-zA-Z0-9_]`.
- `\s`: Any whitespace character (space, tab, newline, and similar).
- `\D`: A character that is not a digit: `[^\d]`.
- `\W`: A nonalphanumeric character: `[^\w]`.
- `\S`: A nonwhitespace character: `[^\s]`.
- `.`: Any character except for newline.

To invert a set of characters, use a caret (`^`) character after the opening bracket.

The following characters repeat the preceding pattern:

- `+`: Repeat 1 or more times.
- `?`: Repeat 0 or 1 time.
- `*`: Repeat 0 or 1 or more times.
- `{n}`: Repeat exactly n times.
- `{n,m}`: Repeat n to m times.
- `{n,}`: Repeat n or more times.

The pipe character (`|`) denotes a choice between the pattern to its left and the pattern to its
right. Parentheses can be used to limit the part of the pattern that the pipe operator applies to.

### Matches and Groups

The `exec` method of a regular expression returns an object with information about the match (the
match object), or `null` if there is not a match.

The match object has an `index` property that tells where in the string the successful match begins.
Other than that, it looks like (and in fact, is) an array of strings, in which the first element is
the string that was matched, and the rest elements, if there are any, are the texts that match the
subexpressions grouped with parentheses.

When a group does not end up being matched at all (for example, when followed by a question mark),
its position in the output array will hold `undefined`. When a group is matched multiple times,
only the last match ends up in the array.

String values have a `match` method that takes a regular expression object as its argument and
behaves similarly to the `exec` method.

### The `replace` Method

String values have a `replace` method, which can be used to replace part of the string with another
string. The first argument can also be a regular expression, in which case the first match of the
regular expression is replaced. When a `g` option (for global) is added to the regular expression,
all matches in the string will be replaced, not just the first.

When using regular expressions with `replace`, we can refer back to matched groups in the
replacement string (the second argument of `replace`). In the replacement string, `$1`, `$2`, up to
`$9` will be replaced the text that matched against the first, second... up to the ninth group. The
whole match can be referred to with `$&`.

It is also possible to pass a function, rather than a string, as the second argument to `replace`.
For each replacement, the function will be called with the matched groups (as well as the whole
match) as arguments, and its return value will be inserted into the new string.

### Greed

The repetition operators (`+`, `*`, `?`, and `{}`) are greedy, meaning they match as much as they
can and backtrack from there. Putting a question mark after them (`+?`, `*?`, `??`, `{}?`) will
make them nongreedy and start by matching as little as possible, matching more only when the
remaining pattern does not fit the smaller match.

### Dynamically Creating `RegExp` Objects

To dynamically create a `RegExp` object by using some input text, the input text should be properly
escaped. Adding backslashes before alphabetic characters is a bad idea because things like `\b` and
`\n` have a special meaning. But escaping everything that's not alphanumeric or whitespace is safe.

```js
var inputText = ...
var escapedText = inputText.replace(/[^\w\s]/g, '\\$&');
```

### The `search` Method

String values have a `search` method, which accepts a regular expression and returns the first
index on which the expression was found, or -1 when it wasn't found.

But there is no way to indicate that the match should start at a given offset (like the second
argument to string's `indexOf` method).

### Regular Expressions with Global Option

Regular expression objects have properties. One such property is `source`, which contains the
string that expression was created from. Another property is `lastIndex`, which controls where the
next match will start, but only in some limited circumstances:

- It must have the global (`g`) option enabled, and...
- The match must happen through the `exec` method.

If the match was successful, the call to `exec` automatically updates the `lastIndex` property to
point after the match. If no match was found, `lastIndex` is set back to 0, which is the default
value of a newly constructed regular expression object.

When using a global regular expression value for multiple `exec` calls, these automatic updates to
the `lastIndex` property can cause problems.

The global option also changes the way the `match` method on strings works. When called with a
global expression, instead of returning an array similar to that returned by `exec`, `match` will
find all matches of the pattern in the string and return an array containing the matched strings.

```js
// The following match returns an array of 2 strings: [ 'an', 'an' ].
// The returned array does not have any other properties like `index`.
console.log('Banana'.match(/an/g));

// The following match returns a match object, which is an array of 1 string: [ 'an' ].
// The match object also has some properties like `index` and `input`.
// Its toString method returns: [ 'an', index: 1, input: 'Banana' ]
console.log('Banana'.match(/an/));

// The following match returns a match object, which is an array of 2 strings: [ 'an', 'an' ].
// The first string is the whole match, the second is the first group.
// Its toString method returns: [ 'an', 'an', index: 1, input: 'Banana' ]
console.log('Banana'.match(/(an)/));
```

So be cautious with global regular expressions. The cases where they are necessary -- calls to
`replace` and places where you want to explicitly use `lastIndex` -- are typically the only places
where you want to use them.

A common pattern is to scan through all occurrences of a pattern in a string, in a way that gives
us access to the match object in the loop body, by using `lastIndex` and `exec`.

```js
var input = 'A string with 3 numbers in it... 42 and 88.';

// Create a global expression to match a number. By default, its lastIndex is set to 0.
var number = /\b(\d+)\b/g;

// Loop over matches. In each loop, the lastIndex property will be used as the starting
// point of the match, and will be updated to point after the current match if successful.
// The loop stops when there's no more matches.
var match;
while (match = number.exec(input)) {
  console.log('Found', match[1], 'at', match.index);
}
// Prints:
// Found 3 at 14
// Found 42 at 33
// Found 88 at 40
```

### International Characters

For historical reasons, JavaScript's regular expression does not support international characters
well. For example, a word character (`\w`) does not match non-Latin alphabet, whilst whitespace
(`\s`) does match all characters that the Unicode standard considers whitespace.


## Modules

Functions are the only things in JavaScript that create a new scope. So we can use functions as
namespaces to create private (local) properties and return an interface containing public properties
(values and functions), wrapped in an object.

```js
var utils = function() {
  // Create a private property which is visible to all nested functions
  // but hidden from the outside.
  var privateProperty = ...
  // Return public functions wrapped in an object.
  return {
    foo: function() { ... },
    bar: function() { ... }
  };
}();  // Immediately call the unnamed function to get its return value.

utils.foo();
utils.bar();
```

A convenient alternative is to declare an object (conventionally named `exports`) and add
properties to it whenever we are defining something that needs to be exported.

In the following example, the unnamed function that creates an interface object will take the
interface object as an argument, allowing code outside of the function to create it and store it in
a variable. Note that outside of a function, `this` refers to the global scope object.

```js
(function(exports) {
  var privateProperty = ...
  exports.foo = function() { ... };
  exports.bar = function() { ... };
})(this.utils = {});
```

### Evaluating Data as Code

The `eval` function executes a string of code in the current scope. It returns the completion value
of evaluating the given code, or `undefined` if the completion value is empty.

A better way of interpreting data as code is to use the `Function` constructor. This takes two
arguments: a string containing a comma-separated list of argument names, and a string containing
the function's body. It creates and returns a `function` value.

### Require

Our goal is a `require` function that, when given a module name, will load that module's file (from
disk or the Web, depending on the platform we are running on) and return the appropriate interface
value.

The module file contains only the function body, and it assumes that an interface object called
`exports` is passed in as the only argument.

A minimal implementation of `require`:

```js
function require(name) {
  // Create a new function by evaluating the module file content.
  var code = new Function('exports', readFile(name));
  var exports = {};
  code(exports);
  return exports;
}
```

To load a module `util-module` and call its exported functions:

```js
var utils = require('util-module');
utils.foo();
utils.bar();
```

The content of `util-module.js`:

```js
// Because the content of this file is evaluated inside a function body in which
// a local scope is created, all variables will be local and hidden from the outside.
var privateProperty = ...

// For anything that needs to be exported to the outside, assign it to `exports`.
exports.foo = function() { ... };
exports.bar = function() { ... };
```

There are two places to improve in the minimal implementation of `require`:

1. Cache the loaded module so it will not be called multiple times.
2. Allow module to directly export a value other than the `exports` object.

```js
function require(name) {
  // Check in cache to avoid loading the same module multiple times.
  if (name in require.cache) {
    return require.cache[name];
  }

  // Evaluate the content of the module as a function body, where the function
  // takes 2 arguments: `exports` and `module`:
  //
  // - If the module wants to export several values, it can add them as
  //   properties of the `exports` interface object.
  // - If the module only wants to export one single value, it can overrides
  //   the `module.exports` property by assigning it to the exported value.
  var code = new Function('exports, module', readFile(name));
  var exports = {};
  var module = {exports: exports};
  code(exports, module);

  // After the module is loaded and evaluated, `module.exports` is the exported
  // interface object, which may or may not be the original `exports` object
  // that was passed into the module.
  require.cache[name] = module.exports;
  return module.exports;
}
require.cache = Object.create(null);
```

To illustrate the second point, imagine that a module `dummy` wants to export one single function,
and can be used via `require` as the following:

```js
var dummy = require('dummy');
dummy();
```

With the improved `require` function, the `dummy.js` is defined as the following:

```js
var privateProperty = ...

// Override `module.exports` to assign it to the single exported function.
module.exports = function() { ... };
```

This style of module system is called *CommonJS modules*, after the pseudo-standard that first
specified it. It is built into the Node.js system.

### Slow-loading Modules

Reading a file (module) from the Web is a lot slower than reading it from the hard disk.

One way to work around this problem is to run a program like [Browserify](http://browserify.org/)
on your code before you serve it on a web page. This will look for calls to `require`, resolve all
dependencies, and gather the needed code into a single big file. The website itself can simply load
this file to get all the modules it needs.

Another solution is to wrap the code that makes up your module in a function so that the module
loader can first load its dependencies in the background and then call the function, initializing
the module, when the dependencies have been loaded. That is what the *AMD (Asynchronous Module
Definition)* module system does.

The [RequireJS](http://requirejs.org/) project provides a popular implementation of AMD module
loader. The syntax for creating an AMD module is:

```js
define(['dep1', 'dep2'], function(dep1, dep2) {
  var privateProperty = ...
  return {
    foo: function() { ... },
    bar: function() { ... }
  };
});
```

The AMD module has 2 dependencies: `dep1` and `dep2`. The `define` function will firstly load the
dependencies, and once loaded, call its second argument with the loaded modules. The returned value
is the exported interface of the AMD module.
