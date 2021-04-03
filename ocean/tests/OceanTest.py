# https://github.com/koalalorenzo/python-digitalocean
# https://ao.gl/how-to-package-a-python-app-pip-for-pypi/
# https://docs.python.org/3/library/unittest.html
# https://developers.digitalocean.com/documentation/

import unittest

# Helps in ignoring resource warnings - due to a flaw in unittest
# https://stackoverflow.com/questions/26563711/disabling-python-3-2-resourcewarning#26620811
import warnings
warnings.simplefilter("ignore", ResourceWarning)
def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test

exec(open("../classes/OceanDependency.py").read())
exec(open("../classes/OceanDroplet.py").read())


class OceanTest(unittest.TestCase):
    
    # TODO:
    # Test ssh key deletion, creation, and upload
    # Check we don't keep uploading the same key
    
    # Auto create an "Ocean" project if it doesn't exist (OceanDependency)

    @ignore_warnings
    def test_ChecksIfProgramExists(self):
        result = shutil.which('ssh')
        self.assertTrue(result != None)
    
    @ignore_warnings
    def test_ChecksIfProgramMissing(self):
        result = shutil.which('sshasdf')
        self.assertTrue(result == None)
        
    @ignore_warnings    
    def test_FindsSshKeyFile(self):
        key_file = (os.path.expanduser('~') + '/.ssh/id_rsa.pub')
        self.assertTrue(os.path.isfile(key_file) == True)
    
    @ignore_warnings
    def test_NotFindMissingSshKey(self):
        key_file = (os.path.expanduser('~') + '/.ssh/id_rsa.pubasdfasdf')
        self.assertTrue(os.path.isfile(key_file) != True)
    
    @ignore_warnings    
    def test_RandomRegion(self):
        ocean_droplet = OceanDroplet()
        result = ocean_droplet.randomise_region()
        #print("RANDOM REGION")
        #print(result)
        self.assertTrue(result != None)
    
    @ignore_warnings
    def test_GetsDropletLimits(self):
        ocean_dependency = OceanDependency()
        droplet_limit = ocean_dependency.get_droplet_limit()
        # print('droplet_limit: ' + str(droplet_limit))
        self.assertTrue(droplet_limit != None)
        
    @ignore_warnings
    def test_DropletLimitIsInt(self):
        ocean_dependency = OceanDependency()
        droplet_limit = ocean_dependency.get_droplet_limit()
        self.assertTrue(isinstance(droplet_limit, int))
        
    @ignore_warnings
    def test_GetRegions(self):
        ocean_dependency = OceanDependency()
        manager = digitalocean.Manager(token=ocean_dependency.token)
        regions = manager.get_all_regions()
        regions_array = []
        for region in regions:
            slug = region.slug
            
            regions_array.append(slug)
        string_regions = ", ".join(regions_array)
        # print(string_regions)
        
    @ignore_warnings
    def test_GetSizes(self):
        ocean_dependency = OceanDependency()
        manager = digitalocean.Manager(token=ocean_dependency.token)
        slugs = manager.get_all_sizes()
        slugs_array = []
        for slug in slugs:
            slug = slug.slug
            slugs_array.append(slug)
        string_slugs = ", ".join(slugs_array)
        #print(string_slugs)
        
    @ignore_warnings
    def test_CheckDropletLimit(self):
        ocean_dependency = OceanDependency()
        limit = ocean_dependency.get_droplet_limit()
        number = 11
        self.assertFalse(number < limit)
        
    @ignore_warnings
    def test_CheckImages(self):
        ocean_dependency = OceanDependency()
        manager = digitalocean.Manager(token=ocean_dependency.token)
        images = manager.get_all_images()
        for image in images:
            if image.name != None:
                print(image.name + " # " + str(image.id))

# Run the unit tests        
unittest.main()