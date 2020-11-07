Feature: Query incomplete todos from a list

As a student,
I query the incomplete tasks for a class I am taking,
To help manage my time.

Scenario Outline: Query incomplete todo items given list name (Normal Flow)

Given I have an existing todo list with title "<listTitle>"
And A set of todo items
    | title           | description                             | doneStatus |
    | project part 1  | Create Gherkin feature files            | True       |
    | interview       | Record interview with SE                | False      |
    | class work      | Complete in class exercises this Monday | False      |

When I submit the query for incomplete todo items
Then Only todo items with doneStatus of false should be returned

Examples: Todo List Data
    | listTitle |
    | ecse429   |