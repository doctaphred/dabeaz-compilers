# wasm.py
#
# This file will emit Wasm code from IR Code.

import struct

'''
Web Assembly Encoder
====================

This file directly encodes Wabbit IR code into a Wasm executable file
with no secondary tools.  Doing this is relatively straightforward,
but involves a lot of low-level binary data encoding.   The definitive
reference for this encoding is the Wasm specification at 
https://webassembly.github.io/spec/.   That document is not the easiest
read so a high-level description is given here.  

The code you need to write is not terribly difficult, but there are
a lot of moving parts. So, read through this first.

Primitives
----------
There are four primitive data types used in the encoding:

  unsigned  - Unsigned integer. Encoded as LEB128.
  signed    - Signed integer. Encoded as LEB128.
  f64       - 64-bit float. Encoded as little-endian double precision.
  byte      - An 8-bit byte. Encoded as is.

The following functions are used for these encodings:
'''

def encode_unsigned(value):
    '''
    Produce an LEB128 encoded unsigned integer.
    '''
    parts = []
    while value:
        parts.append((value & 0x7f) | 0x80)
        value >>= 7
    if not parts:
        parts.append(0)
    parts[-1] &= 0x7f
    return bytes(parts)

def encode_signed(value):
    '''
    Produce a LEB128 encoded signed integer.
    '''
    parts = [ ]
    if value < 0:
        # Sign extend the value up to a multiple of 7 bits
        value = (1 << (value.bit_length() + (7 - value.bit_length() % 7))) + value
        negative = True
    else:
        negative = False
    while value:
        parts.append((value & 0x7f) | 0x80)
        value >>= 7
    if not parts or (not negative and parts[-1] & 0x40):
        parts.append(0)
    parts[-1] &= 0x7f
    return bytes(parts)

assert encode_unsigned(624485) == bytes([0xe5, 0x8e, 0x26])
assert encode_unsigned(127) == bytes([0x7f])
assert encode_signed(-624485) == bytes([0x9b, 0xf1, 0x59])
assert encode_signed(127) == bytes([0xff, 0x00])

def encode_f64(value):
    '''
    Encode a 64-bit float point as little endian
    '''
    return struct.pack('<d', value)

'''
Vectors
-------
Sometimes data is encoded into a vector.  A vector consists
of a u32 size followed by the encoded elements.  One common
type is a text name.  This is encoded as a u32 size followed
by the raw bytes of its UTF-8 encoding:

   name : <u32:size><utf8_bytes>

Functions for vector and name encoding have been given below.
'''

def encode_vector(items):
    '''
    A size-prefixed collection of objects.  If items is already
    bytes, it is prepended by a length and returned.  If items
    is a list of byte-strings, the length of the list is prepended
    to byte-string formed by concatenating all of the items.
    '''
    if isinstance(items, bytes):
        return encode_unsigned(len(items)) + items
    else:
        return encode_unsigned(len(items)) + b''.join(items)

def encode_name(value):
    '''
    Encode a text name as a UTF-8 vector
    '''
    return encode_vector(value.encode('utf-8'))

'''
Wasm File Structure
-------------------
A basic .wasm file is encoded into sections.  The following sections
are pertinent to our project.

              |------------------------------|
Magic/Version | b'\x00asm\x01\x00\x00\x00'   |
              |------------------------------|
Section 1     | Function Type Signatures     |
              |------------------------------|
Section 2     | Module Imports               |
              |------------------------------|
Section 3     | Function declarations        |
              |------------------------------|
Section 7     | Module Exports               |
              |------------------------------|
Section 10    | Function code                |
              |------------------------------|

Each section is encoded as a single byte section number followed by
a u32-encoded section length and the raw contents.  
'''

# ----

'''
Function Type Signatures  (Section 1)
-------------------------------------
A type signature describes the input argument types and return value
type of a function.  Wasm uses the following codes to encode value types:

    valuetype := 
          b'\x7f' => i32
          b'\x7e' => i64
          b'\x7d' => f32
          b'\x7c' => f64

A function signature consists of two vectors (argtypes, rettypes)
describing input types and output types.  Both argtypes and rettypes
may be an empty list to indicate no inputs or no return value respectively.
For example, a function like this:

     func add(x int, y int) int {
         return x + y;
     }

Has a signature of ([i32, i32], [i32]).  A single type signature is
encoded as follows:

     typesig ::= b'\x60' + vector<valuetype> + vector<valuetype>

For the signature above, the raw encoding looks like this:

     b'\x60\x02\x7f\x7f\x01\x7f'

Section 1 of the Wasm file consists of a vector of unique type
signatures.  It is only necessary to encode the *unique* signatures.
Suppose you had a file with 4 functions in it like this:

     func add(x int, y int) int { ... }
     func sub(x int, y int) int { ... }
     func mul(x int, y int) int { ... }
     func fact(n int) int { ... }

The signature vector would only contain two entries

   typeidx signature
   ------- -------------------
   0       [[i32, i32], [i32]]
   1       [[i32], [i32]]

The first entry would be used for the first three functions (this
is described below).  Note, the contents of section 1 for these
signatures would look like this:
    
    b'\x02\x60\x02\x7f\x7f\x01\x7f\x60\x01\x7f\x01\x7f'
      ^^^^ ^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^
        |           |                      |
        |           |                      +--> [[i32], [i32]]
        |           |              
        |           +---> [[i32, i32], [i32]]
        |
        +---> # of signatures (2)

'''

# ----

'''
Imports (Section 2)
-------------------
A Wasm module is allowed to import definitions for use.  This is
very similar to the idea of module imports in Python.  Wasm allows
the import of functions, globals, tables, and memory.  For the
project, we are only concerned with functions. 

To import a function, you first need to know its type signature.  This
type signature must be encoded in the "Type Signature" section 1
described above.  You also need to know the index into the type table
(typeidx).  For example, if the imported function had a signature of
([i32], [i32]), it would have typeidx=1 according to the table above.

Each function import is encoded as a record of the following form:

    importrec ::= <modulename:utf8> <name:utf8> b'\x00' <typeidx:u32>

The contents of section 2 are encoded as a vector of import records.

Important note: imported functions are labeled by funcidx integers
starting at 0.  funcidx=0 is the first imported function, funcidx=1
is the second imported function, and so forth.  These funcidx
labels are important when making function calls in the generated machine
code.
'''
# ----

'''
Function Declarations (Section 3)
---------------------------------
Section 3 of a Wasm module is a vector of type signatures
corresponding to the functions defined in the module (not imports).  
It is vector typeidx integers. For example, if you had these
functions:

     func add(x int, y int) int { ... }
     func sub(x int, y int) int { ... }
     func mul(x int, y int) int { ... }
     func fact(n int) int { ... }

Section 1 would have these type signatures:

   typeidx signature
   ------- -------------------
   0       [[i32, i32], [i32]]
   1       [[i32], [i32]]

Sction 3 would be a vector that looks like this:

   [0, 0, 0, 1]

Functions are identified by funcidx integers.  For functions
defined inside the module (not imported), numbering starts
*after* all of the functions in the import section.  For
example, if there were two imported functions, the four
functions above would have funcidx values of [2, 3, 4, 5].
These numbers are used in function calls and exports.
'''

# ----

'''
Memory (Section 5)
------------------
Section 5 encodes memory the requirements.  It's a vector of
memory specifiers, each have a minimum and optional maximum
like this:

   memtype ::=  \x00 <u32:min>
            |   \x01 <u32:min> <u32:max>

The min and max are specified in pages.  Each page is 64Kb. 
At this time, only one memory section can be specified.
'''

# ----

'''
Globals (Section 6)
-------------------
The globals section is for global variables. 
'''

# ----

'''
Module Exports (Section 7)
--------------------------
For functions to be visible from JS, they need to be exported.
The exports section can export functions, globals, tables, and memory.
For our purposes, we are only interested in functions.  
Each function export is a record of the following form:

    <name:utf8> b'\x00' <funcidx:u32>

The contents of section 7 are encoded as a vector of export records.
'''

# ----

'''
Function Code (Section 10)
--------------------------
The raw assembly code for various functions is contained in this
section.  The order and number of functions must exactly match
the number of entries in the Function Declaration Section 3.
The encoding of this part is a bit tricky because there are
multiple parts, nested within each other.

The section is encoded as a vector of code records. A
code record represents the raw encoding of a function 
and has the following form:

    code ::= <u32:size> <func>

The size is the size (in bytes) of the function function
that follows.

The associated <func> includes declarations of local variables
<locals> and the raw instructions <expr>.

    func ::= <vector(locals)> <expr>

The <locals> part is a vector of local variable record. A local
variable record encodes a set of local variables of the *same* type.
It's encoded as:

    locals ::= <u32:count> <valuetype>

This is potentially very confusing, but here's a concrete
example. Suppose you had a function like this:

    func f(x int, y int) int {
         var a int;
         var b int;
         var c float;
         ...
    }

The local variables to this are "a", "b", and "c".  These locals
are represented as follows:

    [ (2, i32), (1, f64) ]
      ^^^^^^^^  ^^^^^^^^
         |         + 1 local of type 'f64'
         |
      2 locals of type 'i32'

When fully encoded, the locals would look like this:

      b'\x02\x02\x7f\x01\x7c'
        ^^^^ ^^^^^^^ ^^^^^^^^
         |      |        |
         |      |        +-> 1 f64 local
         |      |  
         |      +-> 2 i32 locals
         |
         +-> 2 entries

The <expr> part of a function is the raw Wasm instructions for the
function.  These appear immediately after the locals.  The
instructions must be terminated by a b'\x0b' opcode to end the block.
'''

# ----
