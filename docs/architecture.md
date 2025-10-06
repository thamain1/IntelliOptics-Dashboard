# IntelliOptics Architecture

A full architecture write-up will follow once the edge worker is brought into the monorepo in
reviewable slices. This placeholder tracks the decision to stage the edge import to avoid binary
assets that break PR creation. The Python SDK has been restored as a trimmed client + model package
so shared contracts can evolve alongside the API work without reintroducing the large, generated
artifacts that previously blocked PR tooling.
