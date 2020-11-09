Feature: Change Task Description

  As a student, I want to change a task description, to better represent the work to do.

  Background:
#    Given application is running

  Scenario Outline: Change description of a task (Normal Flow)
    Given a todo task exists in the system with title "<taskTitle>"
    And the todo task with title "<taskTitle>" has the description "<oldDescription>"
    When I update the description of the task "<taskTitle>" to "<newDescription>"
    Then task "<taskTitle>" now has the description "<newDescription>"

    Examples:
      | taskTitle | oldDescription | newDescription                                         |
      | A2        | assignment 2   | ecse429 A2, due nov. 17, 2020                          |
      | A5        | tbd            | ecse123 A5, more info will be given in class on Friday |

  Scenario Outline: Add description to a task (Alternate Flow)
    Given a todo task exists in the system with title "<taskTitle>"
    And the todo task with title "<taskTitle>" has no description
    When I update the description of the task "<taskTitle>" to "<newDescription>"
    Then task "<taskTitle>" now has the description "<newDescription>"

    Examples:
      | taskTitle | newDescription                                         |
      | A2        | ecse429 A2, due nov. 17, 2020                          |
      | A5        | ecse123 A5, more info will be given in class on Friday |

  Scenario Outline: Remove description from a task (Alternate Flow)
    Given a todo task exists in the system with title "<taskTitle>"
    And the todo task with title "<taskTitle>" has the description "<oldDescription>"
    When I remove the description of the task "<taskTitle>"
    Then the todo task with title "<taskTitle>" has no description

    Examples:
      | taskTitle | oldDescription |
      | A2        | assignment 2   |
      | A5        | tbd            |

  Scenario Outline: Change the description of a non-existing task (Error Flow)

    Given a task with title "<taskTitle>" does not exist
    When I update the description of the task "<taskTitle>" to "<newDescription>"
    Then I receive a status code "<statusCode>"

    Examples:
      | newDescription | taskTitle | statusCode |
      | assignment 2   | interview | 400        |