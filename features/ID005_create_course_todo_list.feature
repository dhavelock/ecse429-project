Feature: Create course todo list

As a student,
I create a to do list for a new class I am taking,
So I can manage course work.

Scenario Outline: Create course todo list with description (Normal Flow)

Given I am creating a to do list title "<listTitle>"
And I set the description to "<description>"
When I send the request to create the todo list
Then the response should have title "<listTitle>" with description "<description>"

Examples: Todo List Data
    | listTitle | description                         |
    | ecse429   | todo items for Software Validation  |
