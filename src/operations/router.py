from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate, OperationUpdate


router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


@router.get("/")
async def get_operations(
    session: AsyncSession=Depends(get_async_session)
):
    """
    Return all operations in the database.

    Returns:
        JSON response containing the status of the operation and a list of all
        operations in the database.

    Raises:
        HTTPException: If no operations have been added yet, with a status code
            of 204 (No Content) and a detail field indicating that no services
            have been added yet.
    """
    query = select(operation)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="Services have not been added yet"
        )
    return {
        "status": status.HTTP_200_OK,
        "data": result.mappings().all()
    }
    

@router.get("/{id}")
async def get_operation_by_id(
    id: int, 
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a specific operation by its ID from the database.

    Args:
        id: The ID of the operation to be retrieved.

    Returns:
        JSON response containing the status of the operation and the operation data.

    Raises:
        HTTPException: If the operation with the given ID does not exist, with a 
        status code of 404 (Not Found) and a detail field indicating that the 
        operation does not exist.
    """
    query = select(operation).where(operation.c.id == id)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Operation does not exists"
        )
    return {
        "status": status.HTTP_200_OK,
        "data": result.mappings().first()
    }
    

@router.post("/")
async def create_operation(
    new_operation: OperationCreate, 
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new operation in the database.

    Args:
        new_operation: An OperationCreate object containing the operation data to be added.

    Returns:
        JSON response containing the status of the operation and a message indicating
        that the operation has been successfully added.

    Raises:
        HTTPException: If an operation with the same name already exists, with a status code
            of 409 (Conflict) and a detail field indicating that an operation with the same
            name already exists.
    """
    try:
        stmt = insert(operation).values(**new_operation.model_dump())
        result = await session.execute(stmt)
        print(result)
        await session.commit()
        return {
            "status": status.HTTP_201_CREATED,
            "message": "The service has been successfully added"
        }
    except IntegrityError:
        raise HTTPException(
            status_code=409, 
            detail="An operation with this name already exists"
        )

@router.put("/{id}")
async def update_operation_by_id(
    id: int, 
    updated_operation: OperationUpdate, 
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing operation in the database.

    Args:
        id: The ID of the operation to be updated.
        updated_operation: An OperationUpdate object containing the operation data to be updated.

    Returns:
        JSON response containing the status of the operation and a message indicating
        that the operation has been successfully updated.

    Raises:
        HTTPException: If the operation with the given ID does not exist, with a status code
            of 404 (Not Found) and a detail field indicating that the operation does not exist.
    """
    stmt = update(operation).where(operation.c.id == id).values(**updated_operation.model_dump())
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Operation does not exists"
        )
    await session.commit()
    return {
        "status": status.HTTP_200_OK, 
        "message": "The service has been successfully updated"
    }


@router.delete("/{id}")
async def delete_operation_by_id(
    id: int, 
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete an existing operation from the database.

    Args:
        id: The ID of the operation to be deleted.

    Returns:
        JSON response containing the status of the operation and a message indicating
        that the operation has been successfully deleted.

    Raises:
        HTTPException: If the operation with the given ID does not exist, with a status code
            of 404 (Not Found) and a detail field indicating that the operation does not exist.
    """
    stmt = delete(operation).where(operation.c.id == id)
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Operation does not exists"
        )
    await session.commit()
    return {
        "status": status.HTTP_200_OK,
        "message": "The service has been successfully deleted"
    }
