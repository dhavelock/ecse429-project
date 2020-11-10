Feature: Change the priority of a task

  As a student, I want to adjust the priority of a task, to help better manage my time.

    Background:
    Given a "HIGH" priority category exists in the system
    And a "MEDIUM" priority category exists in the system
    And a "LOW" priority category exists in the system

  Scenario Outline: Adjust the priority of an existing task (Normal Flow)

    Given a task exists with title "<taskTitle>" and a priority level "<oldPriority>"
    When I adjust the task "<taskTitle>" from "<oldPriority>" priority to "<newPriority>" priority
    Then the task with title "<taskTitle>" should have the "<newPriority>" priority category
    And the "<oldPriority>" priority category should not contain the task "<taskTitle>"

    Examples:
      | oldPriority | newPriority | taskTitle    |
      | LOW         | HIGH        | interview    |
      | MEDIUM      | LOW         | assignment 2 |
      | HIGH        | MEDIUM      | powerpoint 4 |

  Scenario Outline: Change the priority of an existing task, to the same priority it already is (Alternate Flow)

    Given a task exists with title "<taskTitle>" and a priority level "<oldPriority>"
    When I adjust the task "<taskTitle>" from "<oldPriority>" priority to "<oldPriority>" priority
    Then the task with title "<taskTitle>" should have the "<oldPriority>" priority category

    Examples:
      | oldPriority | taskTitle    |
      | LOW         | interview    |
      | MEDIUM      | assignment 2 |
      | HIGH        | powerpoint 4 |

  Scenario Outline: Change the priority of a non-existing task (Error Flow)

    Given a task with title "<taskTitle>" does not exist
    When I adjust the task "<taskTitle>" from "<oldPriority>" priority to "<newPriority>" priority
    Then the "<oldPriority>" priority category should not contain the task "<taskTitle>"
    And the "<newPriority>" priority category should not contain the task "<taskTitle>"

    Examples:
      | oldPriority | newPriority | taskTitle    |
      | LOW         | HIGH        | interview    |
