import unittest
from ..src.ConfigChecker import ConfigChecker


class TestConfigChecker(unittest.TestCase):

    def test_object_creation_with_valid_item(self):
        fake_config = {
                "threshold": 0.2, 
                "max_results_per_article":5, 
                "article_types":['journal-article'], 
        }

        new_fake_config = ConfigChecker(config = fake_config).config


        self.assertTrue(fake_config== new_fake_config, f"Valid item does not pass through!")


    def test_object_creation_with_invalid_item(self):
        fake_config1 = {
                "threshold": 'invalid type!!', 
                "max_results_per_article":' another invalid type!!', 
                "article_types":float(0.4), 
        }
        default1 = {
                "threshold": 0.5, 
                "max_results_per_article":10, 
                "article_types":[], 
        }

        fake_config2 = {
                "threshold": 0.0, 
                "max_results_per_article":2, 
                "article_types":['journal-'], 
        }
        default2 = {
                "threshold": 0.0, 
                "max_results_per_article":2, 
                "article_types":[], 
        }

        fake_config3 = {
                "threshold": [], 
                "max_results_per_article": 1, 
                "article_types":[], 
        }


        default3 = {
                "threshold": 0.5, 
                "max_results_per_article":1, 
                "article_types":[], 
        }

        fake_config4 = {
                "threshold": 0, 
                "max_results_per_article": 10, 
                "article_types":[], 
        }


        default4 = {
                "threshold": 0.5, 
                "max_results_per_article":10, 
                "article_types":[], 
        }

        new_fake_config1 = ConfigChecker(config = fake_config1).config
        new_fake_config2 = ConfigChecker(config = fake_config2).config
        new_fake_config3 = ConfigChecker(config = fake_config3).config
        new_fake_config4 = ConfigChecker(config = fake_config4).config
        self.assertTrue(new_fake_config1== default1, f"Invalid item not converted to default!")
        self.assertTrue(new_fake_config2== default2, f"Invalid item not converted to default!")
        self.assertTrue(new_fake_config3== default3, f"Invalid item not converted to default!")
        self.assertTrue(new_fake_config4== default4, f"Invalid item not converted to default!")
        # self.assertTrue(new_fake_config!= fake_config, f"Invalid item not converted to default! {new_fake_config}")