from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import get_db, PropertyService
from ..schemas.property_schema import PropertyResponse
from ..schemas.price_history_schema import PriceHistoryResponse
from ..schemas.statistics_schema import PropertyStatisticsResponse

router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


@router.get(
        "/search",
        response_model=list[PropertyResponse],
        summary="Pesquisar imóveis",
        description="Método de pesquisa avançada de imóveis, permite o uso de filtros."
)
def search_properties(
    city: str | None = None,
    state: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    db: Session = Depends(get_db)

):
    return PropertyService.search(
        db,
        city=city,
        state=state,
        min_price=min_price,
        max_price=max_price,
        min_area=min_area,
        max_area=max_area
    )

@router.get(
        "/statistics", 
        response_model=PropertyStatisticsResponse,
        summary="Apresenta as estatísticas",
        description="Fornece algumas informações úteis a respeito dos dados obtidos."
)
def get_statistics(db: Session = Depends(get_db)):
    return PropertyService.get_statistics(db)

@router.get(
        "/cities",
        summary="Apresenta uma lista de cidades",
        description="Apresenta uma lista de cidades que estão salvas no banco de dados e possuem imóvel à venda."
)
def get_cities(db: Session = Depends(get_db)):
    return PropertyService.get_cities(db)

@router.get(
        "/states",
        summary="Aprensenta uma lista de estados",
        description="Apresenta uma lista de estados que possuem imóveis à venda."
)
def get_states(db: Session = Depends(get_db)):
    return PropertyService.get_states(db)

@router.get(
        "/{property_id}/history", 
        response_model=list[PriceHistoryResponse],
        summary="Apresenta o histórico de preço",
        description="Apresenta o histórico de preço de uma propriedade a partir de seu ID."
)
def get_price_history(
    property_id: int,
    db: Session = Depends(get_db),
):
    return PropertyService.get_price_history(db, property_id)

@router.get(
        "/{property_id}", 
        response_model=PropertyResponse,
        summary="Apresenta informações sobre uma propriedade",
        description="Apresenta informações sobre uma propriedade específica a partir de seu ID."
)
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    return PropertyService.get_by_id(
        db,
        property_id
    )

@router.get(
        "/", 
        response_model=list[PropertyResponse],
        summary="Apresenta uma lista de todas as propriedades",
        description="Apresenta uma lista com todas as propriedades salvas no banco de dados."
)
def get_properties(db: Session = Depends(get_db)):
    return PropertyService.search(db)