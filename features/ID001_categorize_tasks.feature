Feature: Categorize tasks

    As a student,
    I categorize my tasks as HIGH, MEDIUM or LOW priority,
    So I can better manage my time.


    Scenario Outline: Categorize a task as HIGH priority (Normal Flow)

        Given a todo task exists in the system with title "<todoTitle>"
        And a HIGH priority category exists in the system
        When I categorize the task as HIGH priority
        Then the todo task with title "<todoTitle>" should have the HIGH priority categorization

        Examples: Todo Title
            | todoTitle |
            | ecse429   |

    Scenario Outline: Categorize a task as MEDIUM priority (Normal Flow)

        Given a todo task exists in the system with title "<todoTitle>"
        And a MEDIUM priority category exists in the system
        When I categorize the task as MEDIUM priority
        Then the todo task with title "<todoTitle>" should have the MEDIUM priority categorization

        Examples: Todo Title
            | todoTitle |
            | ecse429   |

    Scenario Outline: Categorize a task as LOW priority (Normal Flow)

        Given a todo task exists in the system with title "<todoTitle>"
        And a LOW priority category exists in the system
        When I categorize the task as LOW priority
        Then the todo task with title "<todoTitle>" should have the LOW priority categorization

        Examples: Todo Title
            | todoTitle |
            | ecse429   |

    Scenario Outline: Categorize a task with existing category as HIGH priority (Alternate Flow)

        Given a category exists in the system with title "<categoryTitle>"
        And a todo task exists with title "<todoTitle>" and category with title "<categoryTitle>"
        And a HIGH priority category exists in the system
        When I categorize the task as HIGH priority
        Then the todo task ith title "<todoTitle>" should have both categories associated with it

        Examples: Titles
            | categoryTitle | todoTitle |
            | Category1     | ecse429   |

    Scenario Outline: Scenario Outline name: No category exists (Failure Flow)

        Given a todo task exists in the system with title "<todoTitle>"
        When I request to add a HIGH priority cartegorization to the task using an invalid id
        Then the todo task should not have any category relations

        Examples: Todo Title
            | todoTitle |
            | ecse429   |
