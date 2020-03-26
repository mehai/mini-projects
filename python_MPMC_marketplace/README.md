Student: Zanfir Mihai-Bogdan \
335CC

# Multiple Producers - Multiple Consumers
This is an implementation for an adapted version of the
multiple producers, multiple consumers problem.

## General approach
Starting from the given skel modules, I implemented the
necesarry methods and added little to none new classes,
functions and methods.

### producer
For the producer, I simply take the input as it is and start
publishing one product at a time in the marketplace in the order
of the given input.
Before anything else, I, of course, register the producer in
the marketplace and use the received producer_id for further
interaction with the marketplace.

### consumer
The consumer is somehow similar. It receives a list of carts,
meaning a list of operations that it needs to do on the marketplace
before cashing out each cart.\
First, it always requests a new cart from the marketplace and starts
executing each operation one item at a time. When the cart has no
more operations, it cashes out and prints the bought items.\
This happens for all carts and then it exits.

### marketplace
Marketplace is the module where all the magic and synchronization
happens. To explain it, I'll divide it in 3 sections as follows:
1. __producers logic__\
Every producer receives an index in the producers list when it
registers in the marketplace. The value represents the items in
the marketplace from its queue. A register_lock is used for sync.

2. __carts logic__ \
Every consumer needs to get a cart before doing any operation
on the marketplace. If there are no free carts available (which
are carts previously used by other customers that cashed out) then
a new cart is created and its index in the carts list is returned.\
To protect all the operations with carts, carts_lock is used.

3. __buffer logic__ \
For this MPMC problem, the buffer is a common dictionary for all
producers with <key, value> as <product, [producer_id]>. When
a producer wants to publish a product in the market, it appends to
the list corresponding to the product key in this dictionary.\
To protect all the operations with the market and also with the
producers list, market_lock is used.

## How to run it

### Usage
Please make sure you've got the requirements
installed in your virtual environment
- to run all tests:
```./run_tests.sh```.
- to run a test:
```python3 test.py <input_file>```.

### Requirements
- dataclasses
- pylint