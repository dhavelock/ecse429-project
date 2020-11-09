Feature: Edit Todo In List

As a student
I mark a task as done on my course to do list
So I can track my accomplishments

Scenario Outline: Mark Task as Done (Normal Flow)

Given a todo task exists in the system with id "<id>" 
And the task has a incomplete done status of "<doneStatus>"
When I request to complete the task
Then the todo task with id "<id>" should be completed

Examples: Todo Data
    | id | doneStatus |
    | 1  | False |

Scenario Outline: Mark Completed Task as Done (Alternate Flow)

Given a todo task exists in the system with id "<id>" 
And the task has a complete done status of "<doneStatus>"
When I request to complete the task
Then the todo task with id "<id>" should be completed

Examples: Todo Data
    | id | doneStatus |
    | 1  | True |

Scenario Outline: Mark Invalid Task as Done (Failure Flow)

Given a todo task does not exist in the system with id "<id>" 
And I request to edit an invalid task id in the system
When I request to complete the task
Then the todo task with invalid "<id>" should not be completed with error message 404

Examples: Todo Data
    | id |
    | 999  |