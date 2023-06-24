from typing import List, Any

from fastapi import APIRouter, Depends

from app import schemas
from app.chain.tmdb import TmdbChain
from app.core.context import MediaInfo
from app.core.security import verify_token
from app.schemas.types import MediaType

router = APIRouter()


@router.get("/info", summary="TMDB详情", response_model=schemas.MediaInfo)
async def tmdb_info(tmdbid: int, type_name: str) -> Any:
    """
    根据TMDBID查询themoviedb媒体信息，type_name: 电影/电视剧
    """
    mtype = MediaType.MOVIE if type_name == MediaType.MOVIE.value else MediaType.TV
    tmdbinfo = TmdbChain().tmdb_info(tmdbid=tmdbid, mtype=mtype)
    if not tmdbinfo:
        return schemas.MediaInfo()
    else:
        return MediaInfo(tmdb_info=tmdbinfo).to_dict()


@router.get("/movies", summary="TMDB电影", response_model=List[schemas.MediaInfo])
async def tmdb_movies(sort_by: str = "popularity.desc",
                      with_genres: str = "",
                      with_original_language: str = "",
                      page: int = 1,
                      _: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    浏览TMDB电影信息
    """
    movies = TmdbChain().tmdb_discover(mtype=MediaType.MOVIE,
                                       sort_by=sort_by,
                                       with_genres=with_genres,
                                       with_original_language=with_original_language,
                                       page=page)
    if not movies:
        return []
    return [MediaInfo(tmdb_info=movie).to_dict() for movie in movies]


@router.get("/tvs", summary="TMDB剧集", response_model=List[schemas.MediaInfo])
async def tmdb_tvs(sort_by: str = "popularity.desc",
                   with_genres: str = "",
                   with_original_language: str = "",
                   page: int = 1,
                   _: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    浏览TMDB剧集信息
    """
    tvs = TmdbChain().tmdb_discover(mtype=MediaType.TV,
                                    sort_by=sort_by,
                                    with_genres=with_genres,
                                    with_original_language=with_original_language,
                                    page=page)
    if not tvs:
        return []
    return [MediaInfo(tmdb_info=tv).to_dict() for tv in tvs]


@router.get("/trending", summary="TMDB流行趋势", response_model=List[schemas.MediaInfo])
async def tmdb_trending(page: int = 1,
                        _: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    浏览TMDB剧集信息
    """
    infos = TmdbChain().tmdb_trending(page=page)
    if not infos:
        return []
    return [MediaInfo(tmdb_info=info).to_dict() for info in infos]