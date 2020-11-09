Feature: Remove course todo list

As a student,
I remove a to do list for a class which I am no longer taking,
To declutter my schedule.

Scenario Outline: Remove to do list with no outstanding todo items (Normal Flow)

Given I have an existing todo list with title "<listTitle>"
When I send the request to remove the todo list
Then The todo list with title "<listTitle>" should not exist

Examples: Todo List Data
    | listTitle |
    | ecse429   |

Scenario Outline: Remove to do list with outstanding todo items (Alternate Flow)

Given I have an existing todo list with title "<listTitle>"
And A set of todo items
    | title           | description                             |
    | project part 1  | Create Gherkin feature files            |
    | interview       | Record interview with SE                |
    | class work      | Complete in class exercises this Monday |

When I send the request to remove the todo list
Then The todo list with title "<listTitle>" should not exist
And The todos should have no project relations

Examples: Todo List Data
    | listTitle |
    | ecse429   |

Scenario Outline: Remove to do list that does not exist (Error Flow)

Given I do not have an existing todo list with id "<id>"
When I send the request to remove the todo list
Then The response should have the error message: "Could not find any instances with projects/<id>"

Examples: Todo List Data
    | listTitle | id |
    | ecse429   | 12 |
