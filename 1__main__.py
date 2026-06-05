import pulumi
import pulumi_github as github

config = pulumi.Config()
github_token = config.require_secret("github_token")
# change to "public" if you want the repository to be publicly visible
repo_visibility = config.get("repo_visibility") or "public"

provider = github.Provider("github-provider", token=github_token)

repo = github.Repository("lab-repo",
    name="pulumi-managed-repo",
    description="Repository managed by Pulumi",
    visibility=repo_visibility,
    auto_init=True,
    opts=pulumi.ResourceOptions(provider=provider)
)

branch_protection = github.BranchProtection("main-protection",
    repository_id=repo.node_id,
    pattern="main",
    enforce_admins=True,
    opts=pulumi.ResourceOptions(provider=provider, depends_on=[repo])
)

pulumi.export("repo_url", repo.html_url)
pulumi.export("branch_protection_id", branch_protection.id)