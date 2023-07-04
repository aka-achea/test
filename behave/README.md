
## Structure
```
+-- features/
|     +-- steps/
|     |    +-- website_steps.py
|     |    +-- utils.py
|     |
|     +-- environment.py      # -- Environment file with behave hooks, etc.
|     +-- signup.feature
|     +-- login.feature
|     +-- account_details.feature
```

## Gherkin description in *.feature
```
# -- SIMPLIFIED GHERKIN GRAMMAR (for Gherkin v6):
# CARDINALITY DECORATOR: '*' means 0..N (many), '?' means 0..1 (optional)
# EXAMPLE: Feature
#   A Feature can have many Tags (as TaggableStatement: zero or more tags before its keyword).
#   A Feature can have an optional Background.
#   A Feature can have many Scenario(s), meaning zero or more Scenarios.
#   A Feature can have many ScenarioOutline(s).
#   A Feature can have many Rule(s).
Feature(TaggableStatement):
    Background?
    Scenario*
    ScenarioOutline*
    Rule*

Background:
    Step*           # Background steps are injected into any Scenario of its scope.

Scenario(TaggableStatement):
    Step*

ScenarioOutline(ScenarioTemplateWithPlaceholders):
    Scenario*       # Rendered Template by using ScenarioOutline.Examples.rows placeholder values.

Rule(TaggableStatement):
    Background?     # Behave-specific extension (after removal from final Gherkin v6).
    Scenario*
    ScenarioOutline*

```

## Background
A background consists of a series of steps similar to scenarios. It allows you to add some context to the scenarios of a feature. A background is executed before each scenario of this feature but after any of the before hooks. It is useful for performing setup operations.

A background section may exist only once within a feature file. In addition, a background must be defined before any scenario or scenario outline.

## Scenarios
Scenarios describe the discrete behaviours being tested. They are given a title which should be a reasonably descriptive title for the scenario being tested.

## Scenario Outlines
An outline includes keywords in the step definitions which are filled in using values from example tables. You may have a number of example tables in each scenario outline.
```
Scenario Outline: Blenders
   Given I put <thing> in a blender,
    when I switch the blender on
    then it should transform into <other thing>

 Examples: Amphibians
   | thing         | other thing |
   | Red Tree Frog | mush        |

 Examples: Consumer Electronics
   | thing         | other thing |
   | iPhone        | toxic waste |
   | Galaxy Nexus  | toxic waste |
```

## Steps 
used in the scenarios are implemented in Python files in the “steps” directory. 

**Given** we put the system in a known state before the user (or external system) starts interacting with the system (in the When steps). Avoid talking about user interaction in givens.

**When** we take key actions the user (or external system) performs. This is the interaction with your system which should (or perhaps should not) cause some state to change.

**Then** we observe outcomes.

The **and** and **but** step types are renamed internally to take the preceding step’s keyword


## Tags
You may also “tag” parts of your feature file. At the simplest level this allows behave to selectively check parts of your feature set.

Running behave ```--tags=slow``` will run just the scenarios tagged ```@slow```.



## Context
When behave launches into a new feature or scenario it adds a new layer to the context, allowing the new activity level to add new values, or overwrite ones previously defined, for the duration of that activity. These can be thought of as scopes. You may also use it to share values between steps.

## Environmental Controls
before_all -> feature-before_tag -> before_feature -> scenario-before_tag -> before_scenario -> before_step -> Step -> after_step -> after_scenario -> scenario-after_tag -> after_feature -> feature-after_tag -> after_all

## Fixtures
Fixtures are provided as concept to simplify this setup/cleanup task in behave.

To use fixture, tag in Feature or Scenario, or call ```user_fixture()```

