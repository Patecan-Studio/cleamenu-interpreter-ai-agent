from pydantic.v1 import BaseModel, Field
from langchain_core.tools import tool

from typing import List, Dict, Any

from ai_agent.cleamenu_service import update_price_of_existed_food, vector_query


class FindStoreByFoodNameInput(BaseModel):
    food_name: str = Field(description="Food's Name in the user's request")

class FindFoodWhenKnownStoreInput(BaseModel):
    store_id: str = Field(description="Store'ID in the user's request")
    food_name: str = Field(description="Food's Name in the user's request")


class FoodNameAndFoodPriceInput(BaseModel):
    food_name: str = Field(description="Food's Name in the user's request")
    food_id: str = Field(description="Food's Id in the that belong to the food in the user's request")
    store_id: str = Field(
        description="The Store in the user's request if it be mentioned. Or if it be not mentioned, this is the Store that has the Menu, in that menu contain the food in the user's request")
    food_price: float = Field(description="Price of the Food in the user's request, that they want to update")


@tool("update_price_of_existed_food", args_schema=FoodNameAndFoodPriceInput)
def tool_update_price_of_existed_food(food_name: str, food_id: str, store_id: str, food_price: float) -> str:
    """Extract the food from user's request and update the price of that food"""
    print(f"{food_name}, {food_id}, {store_id}, {food_price}")
    return update_price_of_existed_food(store_id, food_id, food_price)


@tool("search_food", args_schema=FindFoodWhenKnownStoreInput)
def tool_search_food_by_food_name(store_id: str,food_name: str) -> dict[str, Any] | None:
    """Guest the food's name from user's request."""
    print(f"{food_name}")
    return vector_query(store_id,food_name)


food_tools = [
    tool_update_price_of_existed_food,
    tool_search_food_by_food_name
]
