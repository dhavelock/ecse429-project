Feature: Query incomplete HIGH priority tasks from a list

  As a student, I query all incomplete HIGH priority tasks
  from all my classes, to identity my short-term goals.

  Background:
    Given a "HIGH" priority category exists in the system
    And a "MEDIUM" priority category exists in the system
    And a "LOW" priority category exists in the system

  Scenario Outline: Query incomplete HIGH priority tasks (Normal Flow)

    Given the following tasks exist
      | taskTitle      | project | priorityLevel | doneStatus |
      | project part 1 | ecse111 | HIGH          | True       |
      | interview      | ecse123 | MEDIUM        | False      |
      | class work     | ecse213 | HIGH          | False      |
      | project part 2 | ecse321 | MEDIUM        | False      |
      | take-home      | ecse999 | HIGH          | False      |
      | assignment     | ecse429 | LOW           | True       |

    When I submit a query for "<priorityLevel>" priority level tasks with a done status of "<doneStatus>"
    Then the following list "<tasks>" of task titles is returned

    Examples: Todo List Data
      | doneStatus | priorityLevel | tasks                      |
      | False      | HIGH          | class work,  take-home     |
      | False      | MEDIUM        | interview,  project part 2 |

  Scenario Outline: Query incomplete HIGH priority tasks, but they are all completed (Alternate Flow)

    Given the following tasks exist
      | project | taskTitle      | priorityLevel | doneStatus |
      | ecse429 | project part 1 | HIGH          | True       |
      | ecse419 | interview      | HIGH          | True       |
      | ecse123 | class work     | HIGH          | True       |

    When I submit a query for "<priorityLevel>" priority level tasks with a done status of "<doneStatus>"
    Then I receive an empty list
    And I receive a status code "<statusCode>"

    Examples: Todo List Data
      | doneStatus | priorityLevel | statusCode |
      | False      | HIGH          | 200        |

  Scenario Outline: Query incomplete HIGH priority tasks, but priority category does not exist (Error Flow)

    Given the following tasks exist
      | project | taskTitle      | priorityLevel | doneStatus |
      | ecse429 | project part 1 | HIGH          | False      |
    Given the priority category "<priorityLevel>" has been deleted
    When I submit a query for "<priorityLevel>" priority level tasks with a done status of "<doneStatus>"
    Then I receive an empty list
    And I receive a status code "<statusCode>"

    Examples: Todo List Data
      | doneStatus | priorityLevel | statusCode | 
      | False      | HIGH          | 200        | 