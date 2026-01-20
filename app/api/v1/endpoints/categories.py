"""
Category Endpoints
Category listing operations
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.database.category import Category, CategoryDescription
from app.models.schemas.category import CategoryListResponse, CategoryResponse

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=CategoryListResponse,
    tags=["categories"],
    summary="List categories",
    description="List all active categories (with descriptions) for a given language_id.",
    operation_id="listCategories",
)
def list_categories(
    db: Session = Depends(get_db),
    language_id: int = 1,
) -> CategoryListResponse:
    """
    List all active categories.

    Returns all categories with their descriptions.

    Args:
        db: Database session
        language_id: Language ID for descriptions

    Returns:
        CategoryListResponse: List of categories
    """
    categories = (
        db.query(Category)
        .join(CategoryDescription)
        .filter(
            Category.status == 1,
            CategoryDescription.language_id == language_id,
        )
        .all()
    )

    result = []
    for cat in categories:
        desc = next((d for d in cat.descriptions if d.language_id == language_id), None)
        if desc:
            result.append(
                CategoryResponse(
                    category_id=cat.category_id,
                    name=desc.name,
                    description=desc.description,
                    image=cat.image,
                    parent_id=cat.parent_id,
                )
            )

    return CategoryListResponse(categories=result)
