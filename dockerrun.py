import docker
import argparse


def getENV():
    with open('env.list') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def calcs(ENV):
    client = docker.from_env()
    volume_name = 'myvolume'
    client.volumes.create(name=volume_name)
    volume_config = {volume_name: {'bind': '/data', 'mode': 'rw'}}
    output_path = '/data/output.txt'
    
    container = client.containers.run(
        "mol_similarity:v0.4", 
        environment=ENV, 
        volumes=volume_config,
        detach=True,
    )

    response = container.wait()
    output = container.logs()
    print(output.decode())
    container.remove()

    container = client.containers.run(
        "alpine:latest", 
        command=f"cat {output_path}",
        detach=True,
        volumes=volume_config,
    )
    response = container.wait()
    output = container.logs()
    print(output.decode())

    container.remove()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", action=argparse.BooleanOptionalAction)
    parser.add_argument("--top", action=argparse.BooleanOptionalAction)
    parser.add_argument("--sas", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    sim = args.sim
    top = args.top
    sas = args.sas

    ENV = getENV() + [f"TESTS={sim},{top},{sas}" ]
    print(ENV)
    calcs(ENV)

#docker build -t "mol_similarity:v0.3" .