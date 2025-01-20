Pipeline Strategy - draft proposal

Using GitHub Actions

Branching Strategy: 

- short-lived feature ("Feature-<ticket ID>-<Description>") branches, a development/testing ("Dev") branch and a main ("Main") branch

Branch Protection: 

- PRs required, 2 reviewers, CODEOWNERS file.  

PR pipeline checks: 

1. Hardcoded secrets 
2. SonarQube scan
3. Unit Tests
4. Branch naming convention
5. Generate SBOMs, documentation etc. on PR to Main (or as part of build & deploy pipeline)

#1, #2, #3 are non-breaking for PRs into Dev
#4 is compulsory for both branches

(Build & deploy triggers and exact process will depend on the platforms we use for development, testing and hosting - Python & Pytest has been suggested)

Environments: 
- just Staging & Production due to limited scope of project
