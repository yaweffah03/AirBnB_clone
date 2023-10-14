#!/usr/bin/python3
"""This is the Module for Review class."""

from models.base_model import BaseModel


class Review(BaseModel):
    """Class representing a Review."""
    place_id = ""
    user_id = ""
    text = ""
