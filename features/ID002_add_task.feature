Feature: Add task to course to do list

    As a student,
    I add a task to a course to do list,
    So I can remember it.

    Scenario Outline: Add a new task to course to do list (Normal Flow)

        Given I have an existing to do list with title "<listTitle>"
        When I enter the task title "<taskTitle>"
        And I request to create the task
        And I request to add the task to the to do list
        Then the to do list with title "<listTitle>" should include the task with title "<taskTitle>"

        Examples: Todo List Data
            | listTitle | taskTitle |
            | ecse429   | homework  |

    Scenario Outline: Add a new task with a description to course to do list (Alternate Flow)

        Given I have an existing to do list with title "<listTitle>"
        When I enter the task title "<taskTitle>"
        And I enter the task description "<taskDescription>"
        And I request to create the task
        And I request to add the task to the to do list
        Then the to do list with title "<listTitle>" should include the task with title "<taskTitle>"

        Examples: Todo List Data
            | listTitle | taskTitle | taskDescription                   |
            | ecse429   | homework  | todo item for Software Validation |


    Scenario Outline: Add an existing task to course to do list (Alternate Flow)

        Given I have an existing to do list with title "<listTitle>"
        And I have an existing task with title "<taskTitle>"
        When I request to add the task to the to do list
        Then the to do list with title "<listTitle>" should include the task with title "<taskTitle>"

        Examples: Todo List Data
            | listTitle | taskTitle |
            | ecse429   | homework  |


    Scenario Outline: Add an invalid task to course to do list (Error Flow)

        Given I have an existing to do list with title "<listTitle>"
        When I request to add an invalid task to the to do list
        Then the to do list with title "<listTitle>" should not include any tasks

        Examples: Todo List Data
            | listTitle |
            | ecse429   |