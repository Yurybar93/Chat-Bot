## Selenium java framework


### Installation

- install [java 17](https://www.oracle.com/java/technologies/downloads/)
- install [Gradle 8.5](https://gradle.org/releases/)
- install Allure:
    * 'brew install allure' for Mac
    * 'scoop install allure' for Windows
- install dependencies
    * './gradlew build'


### Run tests

- For run tests using testng need to do actions

  1.Open Settings ->Build,Executions,Deployment ->Build Tools->Gradle
  2.Change Build and run  using to Intellij IDEA

  3.Change Run tests using to intellij IDEA

  4.Apply and Ok
- Run all tests ./gradlew clean test

- Run tests using task ./gradlew clean nameOfTask(task name can be found in build.gradle file)
