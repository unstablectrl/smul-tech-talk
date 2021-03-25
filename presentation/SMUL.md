---
marp: true
paginate: true
theme: smul
color: '#333'
headingDivider: 2
---

# A **smul** python tech talk

## Creating a URL **shurt**ening website

**Author:** João Barreiros (@unstablectrl)
**Company:** Runtime Revolution

## What is a **smul** URL? (1)

`https://www.google.com/search?hl=en&ei=csxIYJX4CsHPgwfj5onYCQ&q=What+is+a+smul+URL%3F&oq=What+is+a+smul+URL%3F&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsANQAFgAYNo7aAFwAXgAgAFxiAFxkgEDMC4xmAEAqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwiV-eSM7aXvAhXB5-AKHWNzApsQ4dUDCAw&uact=5`

<!--
- Save space when displayed, printed, messaged, tweeted, etc.

- Users are less likely to mistype shorter URLs.

- Optimize your links for all devices using mobile deep links

- Measure and track user activity

- link expiration, geo targeting, language, etc
-->

## What is a **smul** URL? (2)

`https://www.google.com/search?hl=en&ei=csxIYJX4CsHPgwfj5onYCQ&q=What+is+a+smul+URL%3F&oq=What+is+a+smul+URL%3F&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsANQAFgAYNo7aAFwAXgAgAFxiAFxkgEDMC4xmAEAqgEHZ3dzLXdpesgBCMABAQ&sclient=...`

⬇

`https://smul.io/4579518`

<!--
transforming a long url in a smaller url that redirects to the original long url
-->

## What is a **smul** URL? (3)

`https://www.google.com/...` → `https://smul.io/4579518`

Base 10 `[0-9]`

`10 ^ 7 = 10 Million`

Base 62 `[A-Z, a-z, 0-9]`

`62 ^ 7 = 3.5 Trillion`

## Solutions?

<!--
if time allows it talk with the audience about possible solutions to create a short unique id
-->

## **Shurt** id (1)

### Solution 1 - Hashing the url

Hashing `https://www.google.com` would give us:

Function | Hash
-------- | ----
Adler32  | 5f890849
CRC32    | 331e5b6b
MD5      | 8ffdefbdec956b595d257f0aaeefd623
SHA-1    | ef7efc9839c3ee036f023e9635bc3b056d6ee2db

<!--
Advantages:
- saves database space -> only needs one index on the database

Disadvantages:
- can create duplicates or collisions

Dealing with collisions:
- create if doesn't exists
- if exists swap some characters or add some to the hash and create another entry
-->

## **Shurt** id (2)

### Solution 2 - Counter

Counter `[0 ... ∞]` → Base 62 encode

`4579518` → `SMUL` → `https://smul.io/SMUL`


<!--
Advantages:
- can create even smaller urls
- guarantee no duplicates or collisions

Disadvantages:
- needs two indexes on the database (the url and the short id)
- needs another service for the counter
-->

## Encoding (1)

```txt
 123456789ABCDEFGH JKLMN PQRSTUVWXYZabcdefghijk mnopqrstuvwxyz
= 58 characters = base58

0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
= 62 characters = base62

0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/
= 64 characters = base64
```

<!--
26 = Hexavigesimal
58 = Octoquinquagesimal - Base58 encoding, a variant of Base62 excluding 0 (zero), I (capital i), O (capital o) and l (lower case L). (removes ambiguous character)
62 = Duosexagesimal
64 = Tetrasexagesimal
-->

## Encoding (2)

<!-- _class: encoding2 -->

Index | Binary | Char | Index | Binary | Char | Index | Binary | Char | Index | Binary | Char
----- | ------ | ---- | ----- | ------ | ---- | ----- | ------ | ---- | ----- | ------ | -----
0     | 000000 | A    | 16    | 010000 | Q    | 32    | 100000 | g    | 48    | 110000 | w
1     | 000001 | B    | 17    | 010001 | R    | 33    | 100001 | h    | 49    | 110001 | x
2     | 000010 | C    | 18    | 010010 | S    | 34    | 100010 | i    | 50    | 110010 | y
3     | 000011 | D    | 19    | 010011 | T    | 35    | 100011 | j    | 51    | 110011 | z
4     | 000100 | E    | 20    | 010100 | U    | 36    | 100100 | k    | 52    | 110100 | 0
5     | 000101 | F    | 21    | 010101 | V    | 37    | 100101 | l    | 53    | 110101 | 1
6     | 000110 | G    | 22    | 010110 | W    | 38    | 100110 | m    | 54    | 110110 | 2
7     | 000111 | H    | 23    | 010111 | X    | 39    | 100111 | n    | 55    | 110111 | 3
8     | 001000 | I    | 24    | 011000 | Y    | 40    | 101000 | o    | 56    | 111000 | 4
9     | 001001 | J    | 25    | 011001 | Z    | 41    | 101001 | p    | 57    | 111001 | 5
10    | 001010 | K    | 26    | 011010 | a    | 42    | 101010 | q    | 58    | 111010 | 6
11    | 001011 | L    | 27    | 011011 | b    | 43    | 101011 | r    | 59    | 111011 | 7
12    | 001100 | M    | 28    | 011100 | c    | 44    | 101100 | s    | 60    | 111100 | 8
13    | 001101 | N    | 29    | 011101 | d    | 45    | 101101 | t    | 61    | 111101 | 9
14    | 001110 | O    | 30    | 011110 | e    | 46    | 101110 | u    |       |        |
15    | 001111 | P    | 31    | 011111 | f    | 47    | 101111 | v    |       |        |

<!--
Bijective numeration is any numeral system in which every non-negative integer can be represented in exactly one way using a finite string of digits.

In mathematics, a bijection, bijective function, one-to-one correspondence, or invertible function, is a function between the elements of two sets, where each element of one set is paired with exactly one element of the other set, and each element of the other set is paired with exactly one element of the first set.
-->

## Encoding (3)

```python
def encode(number):
    if number < 1: return CHARSET[0]
    code = ""
    while number > 0:
        number, remainder = divmod(number, BASE)
        code = CHARSET[remainder] + code
    return code
```

Value for A:

`A=0, AA=00, 9=61, BA=62 (Recommended for maths)`

<!--

We are going to iterate through our number (counter) dividing it into smaller and smaller chunks and for each of these subsets we're going to see to what character our number falls into.

We're going to do that by repeatedly doing and Euclidean division of the number by the BASE.

The remainder is going to be the index that tells us to which character we matched with.

And the quotient will give us the ceiling of the new subset.

Euclidean division – or division with remainder – is the process of dividing one integer (the dividend) by another (the divisor), in a way that produces a quotient and a remainder smaller than the divisor.
-->

## Encoding (4)

```python
def encode(number):
    code = ""
    while number > 0:
        number, remainder = divmod(number - 1, BASE)
        code = CHARSET[remainder] + code
    return code
```

Value for A:

`A=1, AA=63, 9=62, BA=125 (Recommended for crypto)`

## **Smul** with Python

## Packages

![flask](https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png)

![flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/master/_images/flask-sqlalchemy-title.png)

![flask-wtf](https://flask-wtf.readthedocs.io/en/stable/_static/flask-wtf.png)

## Project structure

```tree
smul/
├── static
│   └── style.css
├── templates
│   └── index.html
├── smul.py
└── requirements.txt
```

## Database overview

### Counter

Attribute | Type | Index | Unique | Nullable
--------- | ---- | ----- | ------ | --------
value     | int  | false | false  | false

### Shurt

Attribute | Type | Index | Unique | Nullable
--------- | ---- | ----- | ------ | --------
url       | str  | true  | true   | false
code      | str  | true  | true   | false

## Let's do some coding

## References

<!-- _class: references -->

Url shortening system design
<https://www.geeksforgeeks.org/system-design-url-shortening-service/>

Base 62 encoding definition
<https://en.wikipedia.org/wiki/Base62>

Base 26 encoding explained
<https://www.dcode.fr/base-26-cipher>

Base N conversion algorithms
<https://www.dcode.fr/base-n-convert/>

## Tools

Marp - create slides with Markdown
<https://marp.app/>

Visual Studio Code
<https://code.visualstudio.com/>

## That's all she wrote
