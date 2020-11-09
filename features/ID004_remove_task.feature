Feature: Remove Todo

As a student
I remove an unnecessary task from my course to do list
So I can forget about it

Scenario Outline: Delete Todo (Normal Flow)

Given a todo task exists with id "<id>"
When I request to delete the task with "<id>" 
Then the todo task with id "<id>" should not exist with a response 200 status code

Examples: Todo List Data
    | id |
    | 1  |

Scenario Outline: Delete Todo (Failure Flow)

Given a todo does not exist in the system with id "<id>" 
And I want to delete the task with an invalid id
When I request to delete the invalid task
Then I should see an error message with 404 status code

Examples: Todo List Data
    | id |
    | 999  |