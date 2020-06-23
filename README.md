# Truth Tables

Generate a logical statement with a given number of predicates with a given truth table column.

<!-- MarkdownTOC -->

- [What is a truth table?](#what-is-a-truth-table)
    - [TLDR](#tldr)
- [Generating statements with desired truth tables](#generating-statements-with-desired-truth-tables)
    - [`mike_generator()`](#mike_generator)
        - [Example](#example)
    - [`ivan_generator()`](#ivan_generator)
        - [Example](#example-1)
- [`reducer()`](#reducer)

<!-- /MarkdownTOC -->

<a id="what-is-a-truth-table"></a>
## What is a truth table?

Given some logical predicates **P** and **Q**, and some logical statement involving them along with "and", "or", negations, and parentheses, the statement will have different truth values depending on the truth values of the predicates. 

(Note that a logical statement that includes implications or equivalences can always be rewritten in terms of the operators above.)

For example, if **P** is true and **Q** is false, The statement "**P** and ~**Q**" is true (where the tilde represents negation). The same statement would be false if **P** was false, for example. 

These relationships are normally summarized in a *truth table*. Here's the truth table for the statement above.

**P** | **Q** | **P** and ~**Q**
---|---|---
True | True | False
True | False | True
False | True | False
False | False | False

It is common to simply write T and F rather than "True" and "False", and for our purposes we will represent these with 1 and 0, respectively. So for us, the truth table above looks like this:

**P** | **Q** | **P** and ~**Q**
---|---|---
1 | 1 | 0
1 | 0 | 1
0 | 1 | 0
0 | 0 | 0

By convention, the predicates used are upper-case letters starting from **P** and moving forward in the alphabet (it's rare to encounter logical statements with more than five or six predicates).

Also by convention, truth tables are always organized according to some simple rules:

- The first column represents the truth values of **P**, with all 1s at the top and all 0s at the bottom.
- The second column represents the truth values of **Q**. It's split into its upper and lower halves, which corresponding to the rows in which the first column has 1s and 0s, respectively. Within each half the 1s are at the top and the 0s at the bottom. 
- Proceed in this way for all remaining columns (one column for each predicate)
    + Column n is split into 2^(n-1) pieces corresponding to the groups of rows in which the column to the left has sequences of repeating 1s and 0s. 
    + Within each piece, put 1s in the top half and 0s in the bottom half. 

For example, a truth table for the four-predicate statement "((**P** and **Q**) or ~**R**) and (~**P** or **S**)" looks like this:

**P** | **Q** | **R** | **S** | ((**P** and **Q**) or ~**R**) and (~**P** or **S**)
---|---|---|---|---
1 | 1 | 1 | 1 | 1
1 | 1 | 1 | 0 | 0
1 | 1 | 0 | 1 | 1
1 | 1 | 0 | 0 | 0
1 | 0 | 1 | 1 | 1
1 | 0 | 1 | 0 | 0
1 | 0 | 0 | 1 | 1
1 | 0 | 0 | 0 | 0
0 | 1 | 1 | 1 | 1
0 | 1 | 1 | 0 | 1
0 | 1 | 0 | 1 | 1
0 | 1 | 0 | 0 | 1
0 | 0 | 1 | 1 | 1
0 | 0 | 1 | 0 | 1
0 | 0 | 0 | 1 | 1
0 | 0 | 0 | 0 | 1

<a id="tldr"></a>
### TLDR

The truth table for a statement with n predicates has 2^n rows, corresponding to all the possible combinations of truth values of the predicates.

The truth values of the component predicates are organized in a fixed way by convention, and so we can uniquely associate to each statement a sequence of 2^n 0s and 1s. 

In the large table above, we would associate the sequence `1010101011111111` to the statement "((**P** and **Q**) or ~**R**) and (~**P** or **S**)"


<a id="generating-statements-with-desired-truth-tables"></a>
## Generating statements with desired truth tables

As explained above, to every statement with n predicates we can uniquely associate a string of 2^n 0s and 1s, representing the last column of its truth table.

There are 2^2^n possible sequences of 2^n 0s and 1s, and so for example there are 2^2^3 = 2^8 = 256 possible truth table columns for a three-predicate logical statement, in principle. 

The purpose of this code is to take in a desired truth table column as input, and produce a simple logical statement with that column. 

We include two different ways of doing this: `mike_generator` and `ivan_generator`, explained below. It also includes a function for simplifying logical statements, also explained below. 

<a id="mike_generator"></a>
### `mike_generator()`

The key idea here is that if we're working with n predicates, there are certain "atomic" statements that are true for exactly one combination of truth values of the predicates, and false for all others. Specifically, these are "and" statements involving all of the predicates. 

For example if we're working with three predicates and want a statement that's true exactly when **P** is true, **Q** is true, and **R** is false, we simply conjoin them with ands as follows: "**P** and **Q** and ~**R**". This statement is true exactly under the desired three conditions, and false otherwise. 

Knowing this, and given a desired truth table column, do this:

- Find the rows corresponding to the 1 entries in the column.
- Create the "atomic" and statement corresponding to the truth values of the predicates described by that row.
- "or" them all together to make a statement with the desired column. 

<a id="example"></a>
#### Example

Suppose we want a statement for the column `00101100`. 

Since there are eight characters, we know that we need a three-predicate statement. Let **X** be the desired statement. Then its truth table looks like this:

**P** | **Q** | **R** | **X**
---|---|---|---
1 | 1 | 1 | 0
1 | 1 | 0 | 0
1 | 0 | 1 | 1
1 | 0 | 0 | 0
0 | 1 | 1 | 1
0 | 1 | 0 | 1
0 | 0 | 1 | 0
0 | 0 | 0 | 0

From this we can see the three rows corresponding to 1s in the desired column, and build the corresponding atomic statements (from top to bottom):

- **P** and ~**Q** and **R**
- ~**P** and **Q** and **R**
- **P** and ~**Q** and ~**R**

Therefore, we let **X** be the disjunction of these: 

> **X** = (**P** and ~**Q** and **R**) or (~**P** and **Q** and **R**) or (**P** and ~**Q** and ~**R**)


<a id="ivan_generator"></a>
### `ivan_generator()`

This function works recursively, reducing the number of predicates in the statement at each iteration. 

The base case is that of a one-predicate statement, for which we simply specify the four simplest examples that work.

If the statement has more than one predicate, we leverage the conventional way that truth tables are arranged to break the problem into two of the same sort of problem, but involving statements with one fewer predicate. 

For example, recall that a three-predicate statement **X** will have a truth table structured like this:

**P** | **Q** | **R** | **X**
---|---|---|---
1 | 1 | 1 |  
1 | 1 | 0 |  
1 | 0 | 1 |  
1 | 0 | 0 |  
0 | 1 | 1 |  
0 | 1 | 0 |  
0 | 0 | 1 |  
0 | 0 | 0 |  

In particular, note that in the top half of the rows (the first four in this case) **P** is true, while in the bottom half **P** is false. Also note that if you just look at the **Q** and **R** columns, the entries in the top half are identical to the entries in the lower half.

So given a desired truth table column, suppose we could find a statement **Y** involving only **Q** and **R** whose (four character) truth table column was the top half of the desired column. Note that this is precisely the same problem we're trying to solve in general, but for a statement with one fewer predicate. 

Similarly, suppose we could find a statement **Z**, also involving only **Q** and **R**, whose truth table column was the bottom half of the desired column. Then the following statement would have the desired column:

> **X** = (**P** and **Y**) or (~**P** and **Z**)

In the particular case of a three-predicate statement, **Y** and **Z** would be two-predicate statements, and so the function would call itself and reduce these two questions to four questions about one-predicate statements, hitting the base case. 

<a id="example-1"></a>
#### Example

Suppose as in the earlier example that we want a statement **X** for the column `00101100`. 

As described in the previous section, we can reduce this problem to the problem of finding two two-predicate statements **Y** and **Z**, involving only **Q** and **R**, with the following two truth tables:

**Q** | **R** | **Y**
---|---|---
1 | 1 | 0
1 | 0 | 0
0 | 1 | 1
0 | 0 | 0

**Q** | **R** | **Z**
---|---|---
1 | 1 | 1
1 | 0 | 1
0 | 1 | 0
0 | 0 | 0

The problem of finding **Y** reduces to the problem of finding two one-predicate statements **Y1** and **Y2** , involving only **R**, with the following two truth tables:

**R** | **Y1**
---|---
1 | 0
0 | 0

**R** | **Y1**
---|---
1 | 1
0 | 0

The base case takes care of these two simple problems:

> **Y1** = **R** and ~**R**  
> **Y2** = **R**

Therefore, the following statement has the desired truth table column for **Y**

> **Y** = (**Q** and (**R** and ~**R**)) or (~**Q** and **R**)

Similarly, the problem of finding **Z** reduces to the problem of finding one-predicate statements **Z1** and **Z2** with the following two truth tables:

**R** | **Z1**
---|---
1 | 1
0 | 1

**R** | **Z1**
---|---
1 | 0
0 | 0

Again, the base case takes care of these:

> **Z1** = **R** or ~**R**  
> **Z2** = **R** and ~**R**

Therefore, the following statement has the desired truth table column for **Z**

> **Z** = (**Q** and (**R** or ~**R**)) or (~**Q** and (**R** and ~**R**))

Finally, knowing **Y** and **Z**, we can give an answer for a statement **X** with the desired truth table column:

> **X** = (**P** and **Y**) or (~**P** and **Z**)

or fully written out:

> **X** = (**P** and ((**Q** and (**R** and ~**R**)) or (~**Q** and **R**))) or (~**P** and ((**Q** and (**R** or ~**R**)) or (~**Q** and (**R** and ~**R**))))


<a id="reducer"></a>
## `reducer()`

A logical statement that is always true, regardless of the truth values of its predicates, is called a *tautuology*. One that is always false is called a *contradiction*. 

For example, while working through the `ivan_generator` example above, we used both of these. For example, we used the contradiction "**R** and ~**R**" to as a statement with a truth table column of all 0s, and "**R** or ~**R**" as a statement with a truth table column of all 1s. 

The presence of these tautologies can allow us to simplify logical statements. For example, if **X** is a tautological statement and **P** is a predicate, then The statement "**X** and **P**" is true if and only if **P** is true. 

Tautologies and contradictions can appear in "and" and "or" statements, giving four possibilities, all of which reduce to simpler things. If **X** is a tautology, **Y** is a contradiction, and **P** is any predicate, then:

- "**X** and **P**" is equivalent to "**P**"
- "**X** or **P**" is a tautology.
- "**Y** and **P**" is a contradiction.
- "**Y** or **P**" is equivalent to "**P**"

These simplifications allow us to reduce some complicated-looking logical statements into simpler, equivalent statements. Note that this process might require more than one "pass". For example, consider the statement

> **P** and (**Q** or (**R** or ~**R**))

In the innermost pair of brackets we see the tautology "**R** or ~**R**". The "or" statement "**Q** or (**R** or ~**R**)" that it's a part of is therefore a tautology itself, and in turn the entire statement is simply equivalent to **P**.

The `reducer()` function performs these simplifications as much as it can.

```python
>>> X = 'P and (Q or (R or ~R))'
>>> print(reducer(X))
'P'
```

For example, the very long statement **X** at the end of the example of `ivan_generator()` reduces quite a bit:



```python
>>> X = '(P and ((Q and (R and ~R)) or (~Q and R))) or (~P and ((Q and (R or ~R)) or (~Q and (R and ~R))))'
>>> print(reducer(X))
'((P and (~Q and R)) or (~P and Q))'
```