# Dependency update policy

Dependency CI runs on every pull request and requires its entire verification job to succeed. The protected default branch requires `Dependency CI Gate` from GitHub Actions on an up-to-date branch.

Verified Dependabot PRs are eligible for auto-merge only if every update is a strictly increasing minor or patch in the same numeric major version, including pre-1.0 minor and patch updates (0.x to 0.y and 0.0.x patches). The owner intentionally accepts the risk of breaking changes within major zero, including when registry metadata describes such a bump as compatibility-major. Numeric major changes (including 0.x to 1.0), prereleases, downgrades, ranges, missing or unreliable metadata, container tags, date-based versions and maintainer changes require manual review. Sufficient repository regression coverage and all required CI checks must pass; never bypass branch protection or failing or missing required checks. A successful build is evidence, not a guarantee against every regression.

Major updates may still be proposed by Dependabot for manual review; this policy does not suppress security updates.
