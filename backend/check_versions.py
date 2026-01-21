import pkg_resources

packages = [
    "pydantic",
    "langchain",
    "langchain-core",
    "langchain-openai"
]

print("Installed versions:")
for p in packages:
    try:
        dist = pkg_resources.get_distribution(p)
        print(f"{p}: {dist.version}")
    except pkg_resources.DistributionNotFound:
        print(f"{p}: Not installed")
