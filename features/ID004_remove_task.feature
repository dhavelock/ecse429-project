Feature: Remove Todo

As a student
I remove an unnecessary task from my course to do list
So I can forget about it

Scenario: Delete Todo (Normal Flow)

Given a todo task exists with id "<id>"
When the user requests to delete the task with "<id>" 
Then the todo task with id "<id>" should not exist with a response 200 status code

Scenario: Delete Todo (Failure Flow)

Given a todo task exists with id "<id>"
And the user wants to delete the task with an invalid id
When the user requests to delete the invalid task
Then the user should see an error message with 404 status code
