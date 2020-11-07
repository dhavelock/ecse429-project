Feature: Edit Todo In List

As a student
I mark a task as done on my course to do list
So I can track my accomplishments

Scenario: Mark Task as Done (Normal Flow)

Given a todo task exists in the system with id "<id>" 
And the task has a incomplete done status
When the user requests to complete the task
Then the todo task with id "<id>" should be completed

Scenario: Mark Completed Task as Done (Alternate Flow)

Given a todo task exists in the system with id "<id>" 
And the task has a complete done status
When the user requests to complete the task
Then the todo task with id "<id>" should be completed

Scenario: Mark Invalid Task as Done (Failure Flow)

Given a todo task exists in the system with id "<id>" 
And the user requests to edit an invalid task id in the system
When the user requests to complete the task
Then the todo task with id "<id>" should not be completed with error message 404