import httpx
from fastapi import HTTPException
from httpx import AsyncClient
from starlette import status

from app.core import Settings


class UserServiceClient:
    def __init__(
            self,
            settings: Settings,
            client: AsyncClient,
    ) -> None:
        self.settings = settings
        self.client = client

    @property
    def user_url(self) -> str:
        return (
            f"{self.settings.base_url.user_url}"
            f"{self.settings.base_url.api.prefix}"
            f"{self.settings.base_url.api.v1.prefix}"
        )

    async def get_user_by_id(self, user_id: int):
        try:
            headers = {}
            if self.settings.api_key:
                headers["X-API-Key"] = self.settings.api_key

            response = await self.client.get(
                f"{self.user_url}/user/service/{user_id}",
                headers=headers
            )
            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {user_id} not found in User Service"
                )
            response.raise_for_status()

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"User Service unavailable: {str(e)}"
            )

    async def get_company_by_id(self, company_id: int):
        try:
            headers = {}
            if self.settings.api_key:
                headers["X-API-Key"] = self.settings.api_key
            response = await self.client.get(
                f"{self.user_url}/company/service/{company_id}",
                headers=headers
            )
            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with id {company_id} not found in User Service"
                )
            response.raise_for_status()

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"User Service unavailable: {str(e)}"
            )
