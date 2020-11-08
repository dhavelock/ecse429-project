Feature: Categorize tasks

    As a student,
    I categorize my tasks as HIGH, MEDIUM or LOW priority,
    So I can better manage my time.


    Scenario Outline: Categorize a task as HIGH, MEDIUM or LOW priority (Normal Flow)

        Given a todo task exists in the system with title "<todoTitle>"
        And a "<priorityLevel>" priority category exists in the system
        When I categorize the task as "<priorityLevel>" priority
        Then the todo task with title "<todoTitle>" should have the "<priorityLevel>" priority categorization

        Examples: Todo Title
            | todoTitle | priorityLevel |
            | ecse429   | HIGH          |
            | ecse429   | MEDIUM        |
            | ecse429   | LOW           |


    Scenario Outline: Categorize a task with existing category as HIGH, MEDIUM or LOW priority (Alternate Flow)

        Given a category exists in the system with title "<categoryTitle>"
        And a todo task exists with title "<todoTitle>" and category with title "<categoryTitle>"
        And a "<priorityLevel>" priority category exists in the system
        When I categorize the task as "<priorityLevel>" priority
        Then the todo task with title "<todoTitle>" should have both categories associated with it

        Examples: Titles
            | categoryTitle | todoTitle | priorityLevel |
            | Category1     | ecse429   | HIGH          |
            | Category1     | ecse429   | MEDIUM        |
            | Category1     | ecse429   | LOW           |

    Scenario Outline: Scenario Outline name: No category exists (Failure Flow)

        Given a todo task exists in the system with title "<todoTitle>"
        When I request to add a "<priorityLevel>" priority cartegorization to the task using an invalid id
        Then the todo task should not have any category relations

        Examples: Todo Title
            | todoTitle | priorityLevel |
            | ecse429   | HIGH          |
            | ecse429   | MEDIUM        |
            | ecse429   | LOW           |