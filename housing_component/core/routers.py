from fastapi import APIRouter

from housing_component.health.router import router as health_router
from housing_component.rental_units.router import router as rental_units_router
from housing_component.tenants.router import router as tenants_router
from housing_component.access_points.router import router as access_point_router
from housing_component.access_points.router import sensor_router
from housing_component.rental_agreements.router import router as agreement_router
from housing_component.state.router import router as state_router


pre_router = APIRouter(
    prefix="/pre",
)
pre_router.include_router(health_router)
pre_router.include_router(rental_units_router)
pre_router.include_router(tenants_router)
pre_router.include_router(access_point_router)
pre_router.include_router(sensor_router)
pre_router.include_router(agreement_router)
pre_router.include_router(state_router)
