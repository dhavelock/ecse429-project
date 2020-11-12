Feature: Remove Todo

As a student
I remove an unnecessary task from my course to do list
So I can forget about it

Scenario Outline: Delete Task from Todo List (Normal Flow)

Given I have a todo list with title "<listTitle>"
And the todo list has a task with title "<taskTitle>"
When I request to delete the task with "<taskTitle>" from the todo list
Then the todo task with taskTitle "<taskTitle>" should not exist on the todo list

Examples: Todo List Data
    | listTitle | taskTitle | 
    | ecse429   | homework  |

Scenario Outline: Delete Task (Alternate Flow)

Given I have a todo list with title "<listTitle>"
And the todo list has a task with title "<taskTitle>"
When I request to delete the task with "<taskTitle>" from the system
Then the task will be deleted from the system
And the todo task with taskTitle "<taskTitle>" should not exist on the todo list

Examples: Todo List Data
    | listTitle | taskTitle | 
    | ecse429   | homework  |

Scenario Outline: Delete Todo (Failure Flow)

Given I have a todo list with title "<listTitle>"
And the todo list does not have a task with title "<taskTitle>"
And I want to delete the invalid task with "<taskTitle>" from the todo list
When I request to delete the invalid task
Then I should see an error message with 404 status code

Examples: Todo List Data
    | listTitle | taskTitle |
    | ecse429   | homework  |