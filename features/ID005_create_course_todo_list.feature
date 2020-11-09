Feature: Create course todo list

As a student,
I create a to do list for a new class I am taking,
So I can manage course work.

Scenario Outline: Create course todo list with description (Normal Flow)

Given I am creating a to do list title "<listTitle>"
And I set the description to "<description>"
When I send the request to create the todo list
Then The response field "title" should be "<listTitle>"
And The response should have created a todo id
And The response field "completed" should be "false"
And The response field "active" should be "false"
And The response field "description" should be "<description>"

Examples: Todo List Data
    | listTitle | description                        |
    | ecse429   | todo items for Software Validation |

Scenario Outline: Create course todo list without a description (Alternate Flow)

Given I am creating a to do list title "<listTitle>"
When I send the request to create the todo list
Then The response field "title" should be "<listTitle>"
And The response should have created a todo id
And The response field "description" should be ""
And The response field "completed" should be "false"
And The response field "active" should be "false"

Examples: Todo List Data
    | listTitle |
    | ecse429   |

Scenario Outline: Create course todo list with an ID (Error Flow)

Given I am creating a to do list title "<listTitle>"
And I set the description to "<description>"
And I set the id to "<id>"
When I send the request to create the todo list
Then The response should have the error message: "Invalid Creation: Failed Validation: Not allowed to create with id"

Examples: Todo List Data
    | listTitle | description                        | id |
    | ecse429   | todo items for Software Validation | 12 |
