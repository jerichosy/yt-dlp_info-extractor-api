# Dependency update policy

Dependency CI runs on every pull request and requires its entire verification job to succeed. The protected default branch requires `Dependency CI Gate` from GitHub Actions on an up-to-date branch.

Verified Dependabot PRs are eligible for auto-merge only if every update is a stable, strictly increasing minor or patch in the same major version. Pre-1.0 minor changes, all 0.0.x changes, majors, prereleases, ranges, missing metadata, container tags, date-based versions and maintainer changes require manual review. A successful build is evidence, not a guarantee against every regression.

Major and potentially breaking pre-1.0 updates may still be proposed by Dependabot for manual review; this policy does not suppress security updates.
