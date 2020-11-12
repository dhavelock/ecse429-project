Feature: Edit Todo In List

As a student
I mark a task as done on my course to do list
So I can track my accomplishments

Scenario Outline: Mark Task as Done (Normal Flow)

Given a todo list exists in the system with title "<listTitle>" 
And the list has a task with the title "<taskTitle>" and a False done status
When I request to complete the task
Then the todo task with should be completed

Examples: Todo Data
    | listTitle | taskTitle |
    | ecse429 | homework    |

Scenario Outline: Mark Completed Task as Done (Alternate Flow)

Given a todo list exists in the system with title "<listTitle>" 
And the list has a task with the title "<taskTitle>" and a True done status
When I request to complete the task
Then the todo task with should be completed

Examples: Todo Data
    | listTitle | taskTitle |
    | ecse429 | homework    |

Scenario Outline: Mark Invalid Task as Done (Failure Flow)

Given a todo list exists in the system with title "<listTitle>" 
And the list has a task with the title "<taskTitle>" and a False done status
When I request to complete the task with an invalid done status of "<newDoneStatus>"
Then I receive a status code of 400
And the done status of the todo task with "<taskTitle>" will not be changed

Examples: Todo Data
    | listTitle | taskTitle | newDoneStatus |
    | ecse429 | homework    | invalidDoneStatus |