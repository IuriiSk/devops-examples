# scrips example
import os
import digitalocean

manager = digitalocean.Manager(token=os.environ['DO_TOKEN'])
droplet = digitalocean.Droplet(
    token=os.environ['DO_TOKEN'],
    name='web-server',
    region='fra1',
    image='ubuntu-22-04-x64',
    size_slug='s-1vcpu-1gb',
    backups=False
)
droplet.create()
print(f"Droplet ID: {droplet.id}")