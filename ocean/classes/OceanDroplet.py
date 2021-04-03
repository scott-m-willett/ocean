import digitalocean
import random
import os

from classes import OceanDependency

# For interacting with droplets and droplet creation, and related info for creating a droplet (eg: regions and sizes)
class OceanDroplet:

    # Initialiser
    def __init__(self):
    
        # Only supporting one image type currently
        #self.image = 'ubuntu-20-04-x64'
        
        # Dependencies should be met first
        self.ocean_dependency = OceanDependency.OceanDependency()
        
    def set_droplet_image(self, name):
        id = ""
        manager = digitalocean.Manager(token=self.ocean_dependency.token)
        images = manager.get_all_images()
        for image in images:
            if image.name == name:
                id = image.id
        if id != "":
            print("id value for " + name + " is: " + str(id))
            print("Please manually set the environment variable 'digitalocean_image' to this id value.")
            print("You may need to restart your console, or logoff and back in for the value to be read.")
            os.environ["digitalocean_image"] = str(id)
            self.image = os.environ["digitalocean_image"]
        else:
            print("Image " + name + " not found")
    
    def destroy_droplets(self):
        manager = digitalocean.Manager(token=self.ocean_dependency.token)
        my_droplets = manager.get_all_droplets()
        for droplet in my_droplets:
            droplet.destroy()
        print("All droplets destroyed. It may take a minute to take full effect.")
    
    # Create a droplet
    # Regions are randomised by default unless specified
    # Slug is the lowest spec / cheapest VM unless specified
    def create_droplets(self, name=None, number=1, region=None, size=None):
    
        self.image = os.environ["digitalocean_image"]
    
        region_randomise = False
        
        # Just create one by default
        if number == None:
            number = 1
        # Check limit
        within_limits = self.ocean_dependency.check_limit(self.get_droplet_count(), number)
        
        # If the creation requests will be within limits, create them
        if within_limits == True:
        
            provision_count = 1
            
            while provision_count <= number:
            
                selected_region = None
                # generate name if it isn't specified
                if name == None:
                    name_number = ((self.get_droplet_count()) + 1)
                    name = ("ocean" + str(name_number))
                # Randomise the region if not specified
                if region == None:
                    region_randomise = True
                else:
                    selected_region = region
                if region_randomise == True:
                    selected_region = self.randomise_region() 
                # Choose the cheapest and lowest spec option if nothing is specified    
                if size == None:
                    size = 's-1vcpu-1gb'
                # Set options on the droplet   
                manager = digitalocean.Manager(token=self.ocean_dependency.token)
                keys = manager.get_all_sshkeys()
                droplet = digitalocean.Droplet( token=self.ocean_dependency.token,
                                                name=str(name),
                                                region=selected_region,
                                                image=self.image,
                                                size_slug=size,
                                                ssh_keys=keys,
                                                backups=False)
                # Create the droplet
                droplet.create()
                print("Created droplet: " + str(name))
                provision_count += 1
        
    def get_droplet_ip(self, name):
        ip = ""
        manager = digitalocean.Manager(token=self.ocean_dependency.token)
        my_droplets = manager.get_all_droplets()
        for droplet in my_droplets:
            if droplet.name == name:
                ip = droplet.networks['v4'][1]['ip_address']
        return ip
        
    # May be ways to get regions by the API rather than hard coding / updating
    # https://www.digitalocean.com/docs/platform/availability-matrix/
    def randomise_region(self):
        manager = digitalocean.Manager(token=self.ocean_dependency.token)
        regions = manager.get_all_regions()
        regions_array = []
        for region in regions:
            slug = region.slug
            regions_array.append(slug)
        random_number = random.randint(0,(len(regions_array) - 1))
        selected_region = regions_array[random_number]
        return selected_region
        
    # Return a comma seperated list of region slugs
    def get_regions_comma(self):
        manager = digitalocean.Manager(token=self.ocean_dependency.token)
        regions = manager.get_all_regions()
        regions_array = []
        for region in regions:
            slug = region.slug
            regions_array.append(slug)
        string_regions = ", ".join(regions_array)
        return string_regions
    
    def get_sizes_comma(self):
        manager = digitalocean.Manager(token=self.ocean_dependency.token)
        sizes = manager.get_all_sizes()
        sizes_array = []
        for size in sizes:
            size = size.slug
            sizes_array.append(size)
        string_sizes = ", ".join(sizes_array)
        return string_sizes
        
    # Return the count of current droplets
    def get_droplet_count(self):
        manager = digitalocean.Manager(token=self.ocean_dependency.token)
        number = 0
        my_droplets = manager.get_all_droplets()
        for droplet in my_droplets:
            number += 1
        return number