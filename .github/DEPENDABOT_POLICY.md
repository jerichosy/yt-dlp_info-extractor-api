# Dependency updates and images

Successful builds and all required CI gates are mandatory for auto-merge. Stable same-major semver minor/patch changes, including pre-1.0 changes, qualify when every dependency in a group qualifies. Majors (including 0.x to 1.0), prereleases, downgrades and unreliable metadata remain manual.

Owner-approved exception: yt-dlp (including extras) in this repository may automatically update between valid, strictly increasing YYYY.M.D releases, including year boundaries. This does not apply to other packages or repositories. Required protections remain enforced.

Every push/merge to master builds and publishes ghcr.io/jerichosy/yt-dlp_info-extractor-api:sha-<commit>. After application tests and the image build succeed, the current master image is promoted to :latest for Watchtower. Older builds cannot knowingly promote a superseded master commit. Images use the existing Dockerfile (linux/amd64, port 8001). Configure Watchtower/your Docker host with GHCR pull credentials if the package is private.
