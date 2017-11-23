from copy import deepcopy
from unittest import TestCase

from libs.drf_kebab_case.utils import kebabize, underscoreize


class TransformKeysTestCase(TestCase):
    def setUp(self):
        self.data = [
            {
                'first_key': (
                    [
                        {
                            'second_key': True,
                            'third_key': True,
                        }
                    ],
                    [
                        {
                            'fourth_key': True,
                        }
                    ]
                ),
                'fifth_key': True,
            },
        ]
        self.transformed_data = [
            {
                'first-key': (
                    [
                        {
                            'second-key': True,
                            'third-key': True,
                        }
                    ],
                    [
                        {
                            'fourth-key': True,
                        }
                    ]
                ),
                'fifth-key': True,
            },
        ]

    def test_kebabize(self):
        original_data = deepcopy(self.data)

        transformed_data = kebabize(original_data)

        # Check that original objects wasn't changed
        self.assertEqual(original_data, self.data)

        # Check that transformation works correctly
        self.assertEqual(transformed_data, self.transformed_data)

    def test_underscoreize(self):
        original_data = deepcopy(self.transformed_data)

        transformed_data = underscoreize(original_data)

        # Check that original objects wasn't changed
        self.assertEqual(original_data, self.transformed_data)

        # Check that transformation works correctly
        self.assertEqual(transformed_data, self.data)
