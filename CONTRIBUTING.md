# Contributing

Start from [AGENTS.md](AGENTS.md). Use [START-HERE](START-HERE.md) for a first build and [delivery](docs/agents/delivery.md) for branch/PR permissions. For existing repositories, follow [safe adoption](docs/agents/adoption-and-upgrades.md).

Keep one owner per rule, add only necessary dependencies, preserve unrelated work and report actual verification. Infrastructure checks: `python tools/repo.py check --tests`. Native discovery: [smoke procedure](docs/agents/agent-setup-validation.md). Application checks are separate and must be registered after a real stack exists.

No global model choice, credentials, product framework or auto-deployment belongs in the base template. Choose licensing and third-party rights explicitly before distributing a product. A template's license decision does not automatically license added code, assets or reference data.
